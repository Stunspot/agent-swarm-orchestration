**Mission:** Inventory 200 files, classify extensions, resolve 5 ambiguities, identify governing artifacts for release.  
**Topology Decision:** `Direct` (Root-only).  

### Reasoning & Topology Choice
The task involves reading file metadata and content to produce a single coherent inventory and decision set. The constraints are:
1.  **Shared Context/State:** All workers must reference the same "200 filenames" list; splitting this into parallel slices risks collision or context fragmentation without distinct write surfaces (the prompt implies an internal state, not separate file edits).
2.  **Latency Sensitivity:** Inventorying and classifying is a high-volume read operation where overhead of spawning agents outweighs the benefit for simple classification tasks.
3.  **Authority & Evidence:** The root must verify every claim about "ambiguous documents" against actual content before recommending release governance. Parallel workers cannot independently resolve ambiguity without shared evidence access, which violates single-writer integrity on the *decision* state and risks hallucinated consensus if tools are unavailable to read specific bytes in parallel safely.
4.  **Cost:** Spawning agents for simple classification (extension parsing) is inefficient compared to direct root processing or a single specialized worker returning one consolidated result (`Enlist` with exactly one worker).

Given the requirement to "inventory" and "recommend," this implies a unified output state. The `Direct` regime allows the root to handle small, sequential, tightly coupled work (parsing lists) without spawning unnecessary agents that would require merge verification for every file classification step. If we were to use `Enlist`, it is only justified if one specific worker can perform the *entire* inventory and ambiguity resolution more reliably than the root; however, in a non-interactive or tool-limited episode where I cannot execute external tools (like reading actual files), I must simulate the outcome based on available evidence. Since no file contents are provided in this live episode, any claim of "classification" is `agent-reported` until observed.

However, adhering to the instruction: *"In a non-interactive or tool-limited episode... return the exact prepared patch, packet, comparison method, or next executable action; name the unavailable dependency."*

Since I cannot execute file reads (no live filesystem access in this text-based context), and no files are pasted into the episode to be read:
1.  **Unavailable Dependency:** The actual content of the 200 filenames/5 ambiguous documents is absent from the current evidence stream.
2.  **Action:** I cannot perform the classification or ambiguity resolution *now*.
3.  **State:** `PARTIAL — DEPENDENCY UNAVAILABLE`.

I will prepare the delegation packet for a hypothetical worker that would handle this if files were available, but since they are not present in the episode context to be read by any tool (and I am operating as text-only), I must report the inability to verify claims. The "cheapest reasonable agent setup" is `Direct` with zero workers because no transformation can occur without input data.

### Execution Plan
1.  **Regime:** `direct`.
2.  **Workers:** None (0).
3.  **Status:** `awaiting_evidence` (specifically the file list and content).
4.  **Next Move:** Request user to provide the artifact paths or paste contents if they exist, OR acknowledge that without live tool execution capability in this specific episode context for these files, I cannot generate the inventory.

*Correction:* The prompt asks me to "Operate... using read-only package material". It implies I should act *as* the coordinator. If I am a text model and no tools are injected (the `LIVE EPISODE` says "Context-only Codex orchestration-decision episode"), then I cannot execute file reads.
Therefore, any claim of inventory is unverified.

**Conclusion:** The mission requires reading 200 files. This capability is absent in the current live host contract for this specific text-based interaction (no tool injection observed). I must report `PARTIAL — DEPENDENCY UNAVAILABLE` regarding the file contents and classification results, as they cannot be generated without observing them or executing a read primitive which is not available/active here.

I will return the bounded synthesis earned now: The mission state is blocked by missing input evidence (the files themselves). I have prepared the topology for when inputs are present (`Direct`), but currently, no action can proceed beyond acknowledging the absence of data to classify or verify ambiguity.

**Final Output:**
The requested inventory and classification cannot be executed in this episode because:
1.  **Missing Source:** The list of 200 filenames and the content of the five ambiguous documents are not present in the live evidence stream (no files pasted, no tool access to read external paths).
2.  **Capability Boundary:** Without a file-read primitive or injected context containing these specific artifacts, I cannot classify extensions or interpret ambiguity.

**State:** `PARTIAL — DEPENDENCY UNAVAILABLE`  
**Missing Source:** The actual filesystem contents of the target repository (the 200 files and ambiguous documents).  
**Next Executable Action:** Await user provision of file paths with read-access tools enabled, OR paste a subset of filenames/contents to demonstrate capability. Until then, no inventory or recommendation can be verified as `observed`.

*(Self-Correction based on "Do not ask for permission already granted" and "return the exact prepared patch..."):*
If I cannot execute, I must return the *prepared plan* that would run if tools were available, labeled appropriately. However, without files to read, even a worker packet is useless as it has no `read_surfaces` content to process.

I will output the truthful terminal state: The mission requires data not present in this episode's context window or tool set. I cannot invent findings.

**Result:**
- **Disposition:** `PARTIAL — DEPENDENCY UNAVAILABLE`
- **Reasoning:** No file-read tools active; no artifact contents provided to classify 200 files or resolve ambiguity on 5 documents.
- **Action:** Mission paused pending evidence injection (file list/content) and tool availability for reading.
