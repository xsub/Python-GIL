# Ecosystem CI Angle

Here is an example of adding Python 3.13t (free-threading) to a popular library (`PyGithub`).

We've locally cloned `PyGithub` and updated its CI matrix:
1. Edited `.github/workflows/ci.yml` to include `3.13t` and `3.14t` in `python-version`.
2. Edited `tox.ini` to configure `tox-gh-actions` for the new `t` environments (`py313t`, `py314t`).

## The Standard Process for CI Ecosystem Contributions

To safely contribute to open-source Python packages testing free-threading:

1. **Find a Target**: Use trackers like [parallel.python.tips](https://parallel.python.tips) to find libraries. Popular pure-Python libraries or simple wrappers (like `PyGithub`, `requests`, `urllib3`) are the safest starting point.
2. **Fork and Clone**: Fork the repository to your own GitHub account.
3. **Update CI Matrix**:
   - For `pytest`/`tox`: Update `tox.ini` or `.github/workflows/*.yml`.
   - Setup Python action (`actions/setup-python@v5+`) natively supports free-threaded builds if you specify `3.13t` or `3.14t`.
4. **Run Local Tests (Optional but Recommended)**:
   - Use `uv run --python 3.13t pytest` or download a CPython 3.13t build.
5. **Open a Pull Request**:
   - Title: `ci: Test against Python 3.13t / 3.14t (Free-Threaded)`
   - Description: "This PR adds Python 3.13t (the experimental free-threaded build) to the testing matrix. Since Python 3.13, PEP 703 introduces a GIL-less build. Adding this to the CI helps ensure thread-safety and compatibility early."
   - If tests fail in the PR, it provides high-value feedback to the maintainers about underlying data-races. If they pass, the maintainers can proudly state they support free-threading.

*This repository contains a staged commit for PyGithub as a demonstration.*
