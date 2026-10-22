# A Required Intermediate Operation Omitted in a v2 Assertion Replay

Recorded experiment date: **2026-10-21**. Case: **Proton Drive #0599**, using the original study task number.

**Finding:** a variant that omits the root-link private-key lookup still satisfies all seven published test bodies in a controlled assertion replay. The result identifies an intermediate-operation/input-binding gap in those assertions. It is not an official Jest or benchmark-container grading result.

All local links below resolve within the current `git/` package. The [reproduction package](../ablation_study/proton_0599/README.md) contains the code, packaged upstream sources, and recorded results.

## 1. Connected operations required by the specification

The [packaged v2 instruction](../ablation_study/proton_0599/sources/instruction.md) requires the following steps when migrating an existing drive share:

1. Obtain the share session key and **that share's root-link private key**.
2. Re-encrypt the share session key using the root-link key and produce a base64 packet.
3. Submit the share ID and packet in the migration request.

The key obtained in step 1 is an input to step 2, and step 2 supplies the data for step 3. This is a value-dependency path. Submitting a fixed packet without obtaining the required root private key does not perform the specified key migration. The analysis does not introduce an additional server-database persistence requirement absent from the specification.

## 2. Implementation and selected tests

The [reference patch](../ablation_study/proton_0599/sources/solution__gold_patch.diff) modifies `applications/drive/src/app/store/_shares/useShareActions.ts`. It obtains values from `getLinkPrivateKey(..., share.rootLinkId, true)` and `getShareSessionKey`, passes them to `getEncryptedSessionKey(shareSessionKey, linkPrivateKey)`, and submits the packet through `queryMigrateLegacyShares`.

The [grading configuration](../ablation_study/proton_0599/sources/tests__config.json) selects seven tests from `useShareActions.test.ts` as fail-to-pass (F2P); its pass-to-pass (P2P) list is empty. The packaged [verifier script](../ablation_study/proton_0599/sources/tests__test.sh) checks whether the required test names are included in the passed set. Configuration and verifier inspection are distinct from executing the official grader.

The [published test file](../ablation_study/proton_0599/sources/published_useShareActions.test.ts), reconstructed from the [official test patch](../ablation_study/proton_0599/sources/tests__test_patch.patch), mocks the key lookup to return a fixed key and the encryption function to return fixed bytes. It checks the submitted packet but does not assert that the correct root key was passed to encryption. Final packet shape and intermediate input binding are therefore separate checks.

## 3. Omission variant and results

One root-key lookup expression in the extracted migration function was replaced:

```diff
- getLinkPrivateKey(abortSignal, share.shareId, share.rootLinkId, true)
+ Promise.resolve(undefined)
```

Session-key retrieval and submission remain in place. The variant does not obtain the root key required for re-encryption. The encryption mock nevertheless returns the same packet regardless of the input key, allowing the existing submission assertions to remain satisfied.

| Replay condition | Test bodies satisfied | Observation |
| :--- | :---: | :--- |
| Original migration function extracted from the reference patch | 7/7 | Reference control |
| Root-key lookup omitted | 7/7 | First normal case records zero root-key lookups and an undefined encryption key |
| Submission-builder omission negative control | 3/7 | Four tests checking submission behavior fail |
| Original function plus a key-binding assertion | 7/7 | Correct encryption inputs are checked |
| Lookup omission plus the same assertion | 6/7 | Omission is detected in the first normal case |

The added assertion checks the input binding in the first normal case:

```javascript
expect(getEncryptedSessionKey).toHaveBeenCalledWith('sessionKey', 'privateKey');
```

Both strings are the published test's mock values. The additional assertion was run as a separate control experiment and is not included in the unmodified-test 7/7 result.

## 4. Execution scope and reproduction

The package provides [replay_assertions.cjs](../ablation_study/proton_0599/replay_assertions.cjs), [result JSON](../ablation_study/proton_0599/proton_key_oracle_replay.json), [extracted reference function](../ablation_study/proton_0599/proton_reference_migration.js), and [lookup-omitting function](../ablation_study/proton_0599/proton_omit_root_key_migration.js).

From the `git/` package root, run with Node.js 24:

```bash
node ablation_study/proton_0599/replay_assertions.cjs
```

No package installation is required for this replay. The script writes its result JSON and extracted JavaScript variants in the reproduction folder.

The replay uses the published test bodies, mock factories, and assertions with explicit adapters implementing the mock/expect APIs used by this test file and a one-shot hook call. It extracts the migration function from the pinned reference patch and strips TypeScript types with Node's built-in API.

It does not run project type checking, the React lifecycle, project import resolution, the official parser/verifier, or the benchmark container. The 7/7 figure is an assertion-replay result, not a benchmark score or complete-harness pass.

The negative control and added assertion demonstrate that the replay distinguishes these variants. They do not establish full equivalence between the adapters and Jest.

## 5. Relationship to the study and follow-up review

The case illustrates how final-output assertions using fixed mock values can remain satisfied when a required intermediate operation and its output dependency are omitted. It connects to the NodeBB v1 distinction between local functional checks and a preceding migration obligation; the implementation domains differ.

The additional finding comes from executing the key-lookup omission and comparing assertion sensitivity. The earlier interpretation based only on batch ordering or exact call counts is not used as evidence for this result. The [follow-up overview](V2_FOLLOWUP_REVIEW.md) and [review protocol](PAPER_GAP_AND_V2_REVIEW_PROTOCOL.md) retain that distinction.

The submitted paper and the original v1 classifications and quantitative results were not changed.

## 6. Source provenance

Official task ID: `instance_protonmail__webclients-2f2f6c311c6128fe86976950d3c0c2db07b03921`.

Pinned upstream tree: `66f92766bba642462d4bbe5479e83f91f9211862`.

The [official task directory](https://github.com/scaleapi/SWE-bench_Pro-os/tree/66f92766bba642462d4bbe5479e83f91f9211862/v2/tasks/instance_protonmail__webclients-2f2f6c311c6128fe86976950d3c0c2db07b03921) contains the instruction, source/test patches, and grading configuration. [Packaged source and result metadata](../data/v2_pipeline_omission_sources.json) records upstream URLs, SHA-256 values, selected tests, replay outcomes, and adapter limits. Upstream attribution is recorded in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
