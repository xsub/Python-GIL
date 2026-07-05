# Workflow: How to Execute "Ecosystem CI" PRs

This document outlines the standard operating procedure (Modus Operandi) for contributing to the Python free-threading (no-GIL) ecosystem. By following these steps, you can rapidly test and submit compatibility Pull Requests to popular open-source projects.

## Prerequisite
Ensure you have cloned this repository, as it contains the `patch_ci.py` automation script in the `ecosystem_ci` folder.

---

## 1. Select a Target
The safest starting points are widely used, pure-Python libraries or simple wrappers (e.g., API clients, formatting tools). Avoid massive C-extensions on your first attempt, as they often require deep C-API rewriting rather than just a CI matrix update.

*Tip: Check `incompatible_packages.txt` for ideas on what is currently unverified or failing, but keep in mind that pure Python libraries are the lowest-hanging fruit.*

## 2. Fork and Clone
On GitHub, navigate to the target repository and click **Fork**. Then, clone your fork to your local machine:
```bash
git clone git@github.com:YOUR_USERNAME/TargetLibrary.git
cd TargetLibrary
```

## 3. Run the Automation Script
We have provided a script that automatically parses `.github/workflows/*.yml` and `tox.ini` files to inject the Python `3.13t` and `3.14t` test matrices.

From within your local clone of the target library, run:
```bash
python3 /path/to/Python-GIL/ecosystem_ci/patch_ci.py .
```
*The script will output `[+] Patched workflow: ...` for any files it successfully modifies.*

## 4. Commit and Push
Create a dedicated branch for this change, commit the automated patch, and push it back to your fork:
```bash
git checkout -b test-free-threading
git add .
git commit -m "ci: Test against Python 3.13t/3.14t (free-threaded) build"
git push origin test-free-threading
```

## 5. Open the Pull Request
Go to the target repository on GitHub. You should see a prompt to open a Pull Request from your recently pushed branch. Use the following template for your PR description:

> **Title:** `ci: Add Python 3.13t (free-threaded) to testing matrix`
> 
> **Description:**
> ```markdown
> This PR adds Python 3.13t (the experimental free-threaded build) to the testing matrix. 
> 
> Since Python 3.13, PEP 703 introduces a GIL-less build. Adding this to the CI early helps uncover hidden data-races and ensures thread-safety without the GIL. The `actions/setup-python` action supports `3.13t` out of the box.
> 
> If the tests pass, the project is safely compatible with the free-threaded ecosystem. If they fail, this run will provide high-value logs regarding global mutable state or dependency incompatibilities.
> ```

## 6. Review the Results
Once the PR is opened, GitHub Actions will spin up the `3.13t` build. 
- **If it passes (Green):** The maintainers now know their library supports free-threading.
- **If it fails (Red):** The logs will expose concurrent race conditions or incompatible C-extension dependencies. This failure is incredibly valuable to the maintainers as a diagnostic report.
