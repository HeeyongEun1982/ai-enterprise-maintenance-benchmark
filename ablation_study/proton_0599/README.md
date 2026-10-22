# Proton Drive #0599: required key lookup omitted in an assertion replay

This is a **controlled replay of the published test bodies**, not an official
Jest, benchmark-container, TypeScript-project or verifier/parser execution.

Run with Node.js 24 (no package installation):

```bash
node replay_assertions.cjs
```

The script extracts the migration function from the pinned reference patch,
strips TypeScript types using Node's built-in API, and evaluates the unchanged
published test bodies with explicit mock/assertion and one-shot hook adapters.
It writes `proton_key_oracle_replay.json` and the extracted reference/mutant JS.
The adapters and their limits are documented in the script and result JSON.

| Variant | Published test bodies whose assertions hold |
|---|---:|
| Extracted reference migration | 7/7 |
| Root-link private-key lookup omitted | 7/7 |
| Submission-builder negative control | 3/7 |
| Reference plus one key-binding assertion | 7/7 |
| Lookup-omitting variant plus that assertion | 6/7 |

The mutation replaces
`getLinkPrivateKey(abortSignal, share.shareId, share.rootLinkId, true)` with
`Promise.resolve(undefined)`. The first migration test records zero root-key
lookups and an encryption call receiving an undefined key, yet its packet
assertion still holds because the published encryption mock returns a fixed
packet independently of its arguments. Adding an assertion of the actual
encryption inputs distinguishes the reference and mutant in the same replay.

Source: official SWE-bench Pro v2 task
`instance_protonmail__webclients-2f2f6c311c6128fe86976950d3c0c2db07b03921`,
tree `66f92766bba642462d4bbe5479e83f91f9211862`.
`sources/` contains the unchanged downloaded task artifacts and the complete
test file reconstructed by applying the official test patch. These upstream
artifacts retain their upstream licensing; see `../../THIRD_PARTY_NOTICES.md`.

See `../../evidence/V2_PIPELINE_OMISSION_CASE.md` for the requirement chain,
interpretation, exact scope and source provenance.
