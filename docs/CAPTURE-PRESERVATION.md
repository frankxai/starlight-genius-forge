# Capture preservation proposal

This is an adoption proposal for preserving an original prompt, tags and supplied source locator through a local capture packet and interrupted intake. Genius Forge remains the talent and community product described in its README. The separate Idea Swarm proposal in closed, unmerged PR2 is historical; these files do not establish its adoption or launch.

## Private evaluation

The cockpit is `ui/idea-swarm-cockpit.html`. Paste the original text and tags, then save a full capture packet. Download initiation does not confirm that a file was saved. Where the browser supports the native save picker, completion confirms the browser write operation only. Closing the page can lose an unsaved draft.

Select a saved JSON capture to inspect its preview. Replacement is deliberate and can be undone once on that page. Restore retains the supplied provenance; it does not authenticate the author or prove access to the original conversation.

Evaluate the Python intake in a private disposable copy of this proposal, never against personal notes in a shared Git checkout. Its output directory is relative to the script location: `docs/ideas/`, with issue-body and metadata files under `_outbox/` and retained journals under `_pending/`. These outputs can contain the full prompt. Keep them private and outside publication or staging.

```text
python scripts/idea_swarm_intake.py --packet saved-capture.json
python scripts/idea_swarm_intake.py --recover-id <identifier-printed-by-intake>
```

Packet import cannot be combined with other capture inputs. Recovery refuses a missing, malformed or conflicting journal and does not overwrite different existing output bytes. Retain the journal and original packet when a capture is interrupted. The generated issue body is an unposted local stub; no network call, issue creation, roadmap edit or native conversation resumption occurs.

## Review and integration

The thirteen source and fixture files are the complete v9 proposal composed against main `005d12a63d5a69011f8e4fef8f755b2281560dae`. All 120 scoped cases previously passed in an isolated fixture. They cover packet preservation, ambiguous JSON refusal, transfer lifetime, save/restore and damaged-journal recovery. Controlled DOM fixtures are synthetic evidence.

Independent Critic PASS is required before updating issue4 or a roadmap under the preserved Idea Swarm proposal doctrine. Accepted product placement, current owner integration, real desktop/mobile browser behavior, keyboard use, OS file dialogs, power-loss durability, concurrent writers and path-swap/reparse behavior remain open. The criterion for acceptance is a useful prompt-to-cited-continuation-to-editable-artifact workflow, including reopen/export and interruption recovery, compared with manual copy and transfer. Test counts alone do not close it.
