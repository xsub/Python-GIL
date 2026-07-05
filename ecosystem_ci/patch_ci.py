#!/usr/bin/env python3
"""
Automated CI Patcher for Python Free-Threading
Usage: python3 patch_ci.py /path/to/repository

This script scans a given repository for GitHub Actions workflows and tox.ini files,
and attempts to inject Python 3.13t and 3.14t into the testing matrices.
"""

import os
import sys

def patch_github_workflows(repo_path):
    workflows_dir = os.path.join(repo_path, ".github", "workflows")
    if not os.path.isdir(workflows_dir):
        return
        
    for filename in os.listdir(workflows_dir):
        if not filename.endswith(".yml") and not filename.endswith(".yaml"):
            continue
            
        filepath = os.path.join(workflows_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()
            
        original_content = content
        
        # Simple string replacements for common matrix definitions
        replacements = [
            ('"3.13"', '"3.13", "3.13t"'),
            ("'3.13'", "'3.13', '3.13t'"),
            ('"3.14"', '"3.14", "3.14t"'),
            ("'3.14'", "'3.14', '3.14t'")
        ]
        
        for old, new in replacements:
            if old in content and new not in content:
                content = content.replace(old, new)
                
        if content != original_content:
            with open(filepath, "w") as f:
                f.write(content)
            print(f"[+] Patched workflow: {filepath}")

def patch_tox(repo_path):
    tox_path = os.path.join(repo_path, "tox.ini")
    if not os.path.isfile(tox_path):
        return
        
    with open(tox_path, "r") as f:
        content = f.read()
        
    original_content = content
    
    # Patch envlist py{39,310,311,312,313,314} -> py{...313,313t,314,314t}
    if "313," in content and "313t" not in content:
        content = content.replace("313,", "313,313t,")
    elif "313}" in content and "313t" not in content:
        content = content.replace("313}", "313,313t}")
        
    if "314," in content and "314t" not in content:
        content = content.replace("314,", "314,314t,")
    elif "314}" in content and "314t" not in content:
        content = content.replace("314}", "314,314t}")

    # Patch gh-actions mappings if tox-gh-actions is used
    if "3.13: py313" in content and "3.13t: py313t" not in content:
        content = content.replace("3.13: py313", "3.13: py313\n    3.13t: py313t")
    if "3.14: py314" in content and "3.14t: py314t" not in content:
        content = content.replace("3.14: py314", "3.14: py314\n    3.14t: py314t")
        
    if content != original_content:
        with open(tox_path, "w") as f:
            f.write(content)
        print(f"[+] Patched tox.ini: {tox_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 patch_ci.py <path_to_repo>")
        sys.exit(1)
        
    repo_dir = sys.argv[1]
    print(f"Scanning {repo_dir} for CI configuration...")
    patch_github_workflows(repo_dir)
    patch_tox(repo_dir)
    print("Done.")
