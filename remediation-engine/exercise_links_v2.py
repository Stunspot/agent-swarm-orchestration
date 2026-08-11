#!/usr/bin/env python3
"""Exercise README documentation links and rendered Pages navigation/links, with a narrow pre-publication Pages exception."""
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json, re, time

ROOT=Path.cwd()
EVIDENCE=ROOT/'evidence';EVIDENCE.mkdir(exist_ok=True)


def fetch(url, attempts=5):
    error=None
    for i in range(attempts):
        try:
            request=Request(url, headers={'User-Agent':'Mozilla/5.0 Nova-public-docs-link-verifier/1.0','Accept':'text/html,image/*;q=0.8,*/*;q=0.5'})
            with urlopen(request, timeout=35) as response:
                if response.status >= 400:
                    raise RuntimeError(response.status)
                response.read(2048)
                return {'url':url,'status':response.status,'final_url':response.geturl()}
        except Exception as exc:
            error=repr(exc);time.sleep(min(1+i,5))
    raise AssertionError(f'linked destination failed: {url}: {error}')


def readme_links(skip_pages_prefix=None):
    text=(ROOT/'README.md').read_text(encoding='utf-8')
    found=[]
    for match in re.finditer(r'!?\[([^]]*)\]\(([^)]+)\)', text):
        found.append({'label':match.group(1),'href':match.group(2).strip()})
    results=[]
    for item in found:
        href=item['href']
        if skip_pages_prefix and href.rstrip('/') == skip_pages_prefix.rstrip('/'):
            results.append({**item,'result':'deferred-until-exact-pages-deployment'})
        elif href.startswith('#'):
            results.append({**item,'result':'in-page-anchor-declared'})
        elif href.startswith(('https://','http://')):
            results.append({**item,**fetch(href)})
        elif href.startswith(('mailto:','tel:')):
            results.append({**item,'result':'non-http-route'})
        else:
            path=unquote(urlsplit(href).path)
            target=(ROOT/path).resolve()
            assert ROOT.resolve() in target.parents or target == ROOT.resolve(), href
            assert target.exists(), f'dead README-relative link: {href}'
            results.append({**item,'result':'local-target-exists','target':str(target.relative_to(ROOT))})
    assert results, 'README exposes no links'
    return results


def pages_links(url):
    from playwright.sync_api import sync_playwright
    output={'url':url,'navigation':[],'external':[]}
    with sync_playwright() as p:
        browser=p.chromium.launch()
        page=browser.new_page(viewport={'width':1280,'height':900})
        response=page.goto(url, wait_until='domcontentloaded', timeout=60000)
        assert response and response.status < 400
        page.wait_for_selector('main', timeout=30000)
        page.wait_for_timeout(1000)
        nav=page.locator('nav a')
        assert nav.count() >= 7
        for index in range(nav.count()):
            href=nav.nth(index).get_attribute('href')
            text=nav.nth(index).inner_text().strip()
            assert href and href.startswith('#'), (text,href)
            page.locator(f'nav a[href="{href}"]').click()
            page.wait_for_timeout(120)
            assert page.evaluate('location.hash') == href
            target=page.locator(href)
            assert target.count() == 1
            box=target.bounding_box()
            assert box and box['width'] > 0 and box['height'] > 0
            output['navigation'].append({'text':text,'href':href,'target_box':box})
        hrefs=page.eval_on_selector_all('a[href]', 'nodes => [...new Set(nodes.map(n => n.href))]')
        current_origin=page.evaluate('location.origin')
        current_path=page.evaluate('location.pathname')
        browser.close()
    for href in hrefs:
        if href.startswith(('mailto:','tel:')):
            continue
        parts=urlsplit(href)
        if parts.scheme not in ('http','https'):
            continue
        if f'{parts.scheme}://{parts.netloc}' == current_origin and parts.path == current_path and parts.fragment:
            continue
        output['external'].append(fetch(href))
    assert output['external'], 'Pages exposes no linked documentation routes'
    return output


def main():
    parser=ArgumentParser();parser.add_argument('--url',required=True);parser.add_argument('--allow-unpublished-pages',action='store_true');args=parser.parse_args()
    slug=ROOT.name
    expected_pages=f'https://stunspot.github.io/{slug}/' if args.allow_unpublished_pages else None
    result={'readme':readme_links(expected_pages),'pages':pages_links(args.url),'verdict':'PASS'}
    (EVIDENCE/'link-exercise.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
