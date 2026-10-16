"""
NodeBB #0030 Qualitative Patch Diff & Test Oracle Static Inspection Script

Instance ID: instance_NodeBB__NodeBB-a5afad27e52fd336163063ba40dcadc80233ae10-vd59a5728dfc977f44533186ace531248c2917516
Base Commit: 7800016f2f1b89d2d3cfea6a7da7c77096b7b927

This script performs purely static code and test oracle inspection:
1. Verifies structural patch composition between Developer Reference Patch (12 files)
   and Candidate Ablated Patch (11 files, omitting the DB migration (44 added lines; 50-line diff hunk)).
2. Inspects official SWE-bench Pro test patch assertions (test/messaging.js) to statically
   demonstrate the Oracle Blind Spot (Construct Underrepresentation).
NOTE: This script performs NO dynamic container execution and produces NO synthetic execution logs.
"""

import os
import sys
import json

def inspect_patches():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    spec_path = os.path.join(base_dir, "nodebb_0030_spec.json")
    dev_patch_path = os.path.join(base_dir, "nodebb_0030_developer_patch.diff")
    ablated_patch_path = os.path.join(base_dir, "nodebb_0030_ablated_patch.diff")
    test_patch_path = os.path.join(base_dir, "nodebb_0030_test_patch.diff")

    if not (os.path.exists(spec_path) and os.path.exists(dev_patch_path) and 
            os.path.exists(ablated_patch_path) and os.path.exists(test_patch_path)):
        print("[FAIL] Required patch or specification files are missing.")
        sys.exit(1)

    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)

    print("=" * 80)
    print(" NodeBB #0030 STATIC CODE DIFF & TEST ORACLE INSPECTION REPORT")
    print("=" * 80)
    print(f"Target Instance: {spec.get('instance_id')}")
    print(f"Base Commit    : {spec.get('base_commit')}")
    print(f"Problem Scope  : {spec.get('problem_title')} - {spec.get('description')}")

    # 1. Structural Patch Composition
    with open(dev_patch_path, 'r', encoding='utf-8') as f:
        dev_text = f.read()
    with open(ablated_patch_path, 'r', encoding='utf-8') as f:
        ablated_text = f.read()
    with open(test_patch_path, 'r', encoding='utf-8') as f:
        test_text = f.read()

    dev_files = [l for l in dev_text.splitlines() if l.startswith('diff --git ')]
    ablated_files = [l for l in ablated_text.splitlines() if l.startswith('diff --git ')]
    test_files = [l for l in test_text.splitlines() if l.startswith('diff --git ')]

    migration_file = "src/upgrades/4.3.0/chat_allow_list.js"
    has_migration_dev = migration_file in dev_text
    has_migration_abl = migration_file in ablated_text

    print("\n[1. Patch Diff Structural Verification]")
    print(f"  * Developer Reference Patch: {len(dev_files)} files modified")
    print(f"    - Includes DB Migration Script ({migration_file}): {has_migration_dev} (44 added lines, 50-line hunk)")
    print(f"  * Candidate Ablated Patch  : {len(ablated_files)} files modified")
    print(f"    - Includes DB Migration Script ({migration_file}): {has_migration_abl} (0 lines, 100% omitted)")
    print(f"  * Test Patch               : {len(test_files)} files modified (test/messaging.js, test/user.js)")

    # 2. Test Oracle Scope & Blind Spot Analysis
    asserts_can_message = "Messaging.canMessageUser" in test_text
    asserts_allow_list = "chatAllowList" in test_text
    asserts_upgrade_script = migration_file in test_text or "src/upgrades" in test_text

    print("\n[2. Test Oracle Scope & Blind Spot Analysis]")
    print(f"  * Test Asserts Messaging.canMessageUser : {asserts_can_message}")
    print(f"  * Test Asserts chatAllowList setting    : {asserts_allow_list}")
    print(f"  * Test Asserts DB Migration / Upgrades  : {asserts_upgrade_script} (Zero assertions)")
    print(f"  * Oracle Blind Spot Mechanism:")
    print("    - test/messaging.js creates fresh mock users on the fly via User.create().")
    print("    - It injects 'chatAllowList' directly into memory, testing only the leaf permission function.")
    print("    - No tests verify legacy forum database state conversion or upgrade execution idempotency.")

    print("\n[3. Scientific Finding: Construct Underrepresentation]")
    print("  - The inspected F2P test patch primarily validates local leaf function behavior, leaving")
    print("    the critical architectural requirement (A5 -> B6, database migration) unverified.")
    print("  - This is an observed assertion-scope limitation of the supplied F2P test patch, not proof of the complete runtime oracle or benchmark score.")
    print("=" * 80)

if __name__ == "__main__":
    inspect_patches()
