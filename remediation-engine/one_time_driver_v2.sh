#!/usr/bin/env bash
set -Eeuo pipefail

ENGINE_BASE='https://raw.githubusercontent.com/Stunspot/agent-swarm-orchestration/agent/remediation-probe-do-not-merge/remediation-engine'
TRANSPORT_BRANCH="${TRANSPORT_BRANCH:?TRANSPORT_BRANCH is required}"
REPOSITORY="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
SLUG="${REPOSITORY#*/}"

mkdir -p evidence .remediation-runtime
printf '\n/.remediation-runtime/\n/evidence/\n' >> .git/info/exclude

on_exit() {
  rc=$?
  if [[ $rc -ne 0 ]]; then
    python - "$rc" <<'PY' || true
from pathlib import Path
import json, os, sys, time
Path('evidence').mkdir(exist_ok=True)
Path('evidence/blocker.json').write_text(json.dumps({
  'repository': os.environ.get('GITHUB_REPOSITORY'),
  'transport_branch': os.environ.get('TRANSPORT_BRANCH'),
  'exit_code': int(sys.argv[1]),
  'workflow_run': os.environ.get('GITHUB_RUN_ID'),
  'status': 'BLOCKED',
  'recorded_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
}, indent=2)+'\n', encoding='utf-8')
PY
  fi
}
trap on_exit EXIT

printf 'Repository: %s\nTransport branch: %s\n' "$REPOSITORY" "$TRANSPORT_BRANCH" | tee evidence/context.txt

git fetch --no-tags origin main
current_branch="$(git branch --show-current)"
[[ "$current_branch" == "$TRANSPORT_BRANCH" ]] || { echo "BLOCKER: expected $TRANSPORT_BRANCH, got $current_branch" >&2; exit 40; }
branch_parent="$(git rev-parse HEAD^)"
current_main="$(git rev-parse origin/main)"
printf 'branch_parent=%s\ncurrent_main=%s\n' "$branch_parent" "$current_main" | tee evidence/base-proof.txt
[[ "$branch_parent" == "$current_main" ]] || { echo 'BLOCKER: main drifted after transport branch creation.' >&2; exit 41; }

git checkout --detach "$current_main"
[[ "$(git rev-parse HEAD)" == "$current_main" ]]

sudo apt-get update
sudo apt-get install -y --no-install-recommends tesseract-ocr
python -m pip install --disable-pip-version-check pillow imagehash markdown beautifulsoup4 playwright
python -m playwright install --with-deps chromium

for helper in remote_remediate_v3.py verify_publication.py exercise_links_v2.py; do
  curl --fail --silent --show-error --location "$ENGINE_BASE/$helper" -o ".remediation-runtime/$helper"
  [[ -s ".remediation-runtime/$helper" ]]
done
sha256sum .remediation-runtime/* | tee evidence/engine-sha256.txt

REPO_SLUG="$SLUG" python .remediation-runtime/remote_remediate_v3.py | tee evidence/generator-result.json
python .remediation-runtime/verify_publication.py local | tee evidence/local-verification-console.txt

python -m http.server 8765 --directory docs > evidence/local-server.log 2>&1 &
server_pid=$!
cleanup_server() { kill "$server_pid" 2>/dev/null || true; }
trap 'cleanup_server; on_exit' EXIT
for _ in $(seq 1 40); do curl -fsS http://127.0.0.1:8765/ >/dev/null && break; sleep 1; done
python .remediation-runtime/verify_publication.py render-local --url http://127.0.0.1:8765/ | tee evidence/local-render-console.txt
python .remediation-runtime/exercise_links_v2.py --url http://127.0.0.1:8765/ --allow-unpublished-pages | tee evidence/local-link-console.txt
cleanup_server
trap on_exit EXIT

git add README.md CUSTOMER-GUIDE.md SUPPORT.md CONTRIBUTING.md SECURITY.md documentation-manifest.json docs verification .github/workflows/deploy-pages.yml
staged="$(git diff --cached --name-only)"
printf '%s\n' "$staged" | tee evidence/staged-paths.txt
if [[ -n "$staged" ]]; then
  bad="$(printf '%s\n' "$staged" | grep -Ev '^(README\.md|CUSTOMER-GUIDE\.md|SUPPORT\.md|CONTRIBUTING\.md|SECURITY\.md|documentation-manifest\.json|docs/|verification/|\.github/workflows/deploy-pages\.yml)' || true)"
  [[ -z "$bad" ]] || { printf 'BLOCKER: unrelated staged paths:\n%s\n' "$bad" >&2; exit 43; }
  git diff --cached --check
  git config user.name 'Nova Documentation Remediator'
  git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
  git commit -m 'Remediate public documentation and presentation'
  [[ "$(git rev-parse HEAD^)" == "$current_main" ]] || { echo 'BLOCKER: non-atomic commit ancestry.' >&2; exit 44; }
  final_sha="$(git rev-parse HEAD)"
  git push origin HEAD:main
else
  final_sha="$current_main"
fi
printf '%s\n' "$final_sha" | tee evidence/final-commit.txt

raw_url="https://raw.githubusercontent.com/${REPOSITORY}/${final_sha}/README.md"
readme_ready=0
for _ in $(seq 1 50); do
  if curl -fsSL "$raw_url" -o evidence/live-readme.md && cmp -s README.md evidence/live-readme.md; then readme_ready=1; break; fi
  sleep 3
done
[[ "$readme_ready" == 1 ]] || { echo 'LIVE VERIFICATION FAIL: final raw README does not byte-match.' >&2; exit 51; }

export GH_TOKEN="${GH_TOKEN:?GH_TOKEN is required}"
started="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
dispatched=0
for _ in $(seq 1 30); do
  if gh workflow run deploy-pages.yml --repo "$REPOSITORY" --ref main; then dispatched=1; break; fi
  sleep 3
done
[[ "$dispatched" == 1 ]] || { echo 'BLOCKER: exact-main Pages workflow could not be dispatched.' >&2; exit 52; }

run_id=''
for _ in $(seq 1 60); do
  run_id="$(gh run list --repo "$REPOSITORY" --workflow deploy-pages.yml --branch main --event workflow_dispatch --limit 30 --json databaseId,headSha,createdAt --jq ".[] | select(.headSha == \"$final_sha\" and .createdAt >= \"$started\") | .databaseId" | head -n1)"
  [[ -n "$run_id" ]] && break
  sleep 3
done
[[ -n "$run_id" ]] || { echo 'BLOCKER: dispatched Pages run was not observable for the final commit.' >&2; exit 53; }
printf '%s\n' "$run_id" | tee evidence/pages-run-id.txt
gh run watch "$run_id" --repo "$REPOSITORY" --exit-status
gh run view "$run_id" --repo "$REPOSITORY" --json databaseId,status,conclusion,headSha,url,jobs > evidence/pages-deployment-run.json
python - "$final_sha" <<'PY'
import json,sys
run=json.load(open('evidence/pages-deployment-run.json'))
assert run['status']=='completed',run
assert run['conclusion']=='success',run
assert run['headSha']==sys.argv[1],(run['headSha'],sys.argv[1])
PY

pages_url=''
for _ in $(seq 1 50); do
  pages_url="$(gh api "repos/${REPOSITORY}/pages" --jq '.html_url' 2>/dev/null || true)"
  [[ -n "$pages_url" ]] && break
  sleep 3
done
if [[ -z "$pages_url" ]]; then pages_url="https://${GITHUB_REPOSITORY_OWNER,,}.github.io/${SLUG}/"; fi
[[ "$pages_url" == */ ]] || pages_url="${pages_url}/"
printf '%s\n' "$pages_url" | tee evidence/live-pages-url.txt

index_ready=0
for _ in $(seq 1 100); do
  if curl -fsSL "${pages_url}index.html?sha=${final_sha}" -o evidence/live-index.html && cmp -s docs/index.html evidence/live-index.html; then index_ready=1; break; fi
  sleep 5
done
[[ "$index_ready" == 1 ]] || { echo 'LIVE VERIFICATION FAIL: deployed index does not byte-match final docs.' >&2; exit 61; }

for role in readme-hero pages-hero social-card; do
  curl -fsSL "${pages_url}assets/${SLUG}-${role}.png?sha=${final_sha}" -o "evidence/live-${role}.png"
  cmp -s "docs/assets/${SLUG}-${role}.png" "evidence/live-${role}.png" || { echo "LIVE VERIFICATION FAIL: $role bytes differ." >&2; exit 62; }
done

python .remediation-runtime/verify_publication.py live --pages-url "$pages_url" --final-sha "$final_sha" --repo "$REPOSITORY" | tee evidence/live-verification-console.txt
python .remediation-runtime/exercise_links_v2.py --url "$pages_url" | tee evidence/live-link-console.txt
python .remediation-runtime/verify_publication.py result --pages-url "$pages_url" --final-sha "$final_sha" --repo "$REPOSITORY" --pages-run-id "$run_id" | tee evidence/publication-result-console.txt

printf 'PASS %s %s %s\n' "$REPOSITORY" "$final_sha" "$pages_url"
