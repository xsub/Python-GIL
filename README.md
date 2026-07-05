# 🚀 Help test GIL-free Python!

The Python ecosystem is undergoing one of the biggest architectural shifts in its history: **PEP 703 (Making the Global Interpreter Lock Optional)**. 

Starting with Python 3.13 (experimental) and moving toward Python 3.14 (official support), the GIL can be disabled (`python -t`). While pure-Python code mostly works out of the box, thousands of C-extensions and widely used libraries need testing and adaptation for true thread safety.

This repository serves as a practical guide and demonstration for developers who want to contribute to the Free-Threaded (No-GIL) migration effort. Inside, you will find ecosystem checks, known standard-library limitations, and actionable contribution methods.

---

## 📊 Ecosystem Check: Notable Incompatible Libraries

Because this paradigm shifts how thread safety is handled (removing the Global Interpreter Lock), many existing C extensions and third-party libraries face race conditions or incompatibilities until they are updated.

Based on active compatibility tracking (from sources like [parallel.python.tips](https://parallel.python.tips/) and [py-free-threading.github.io](https://py-free-threading.github.io/)), several prominent libraries currently report issues or lack full support for the free-threaded build. In some cases, the installation or import fails outright because the library enforces GIL-only constraints:

- **Core Dependencies**: `cffi` (Fails during install/import in free-threading mode), `cryptography` (Installs, but fails to import without the GIL), `pyopenssl`, `pynacl`
- **Data & ML**: `tensorflow` (Installation/Build barriers), `pydantic-core` (Installs, but fails to import without the GIL), `scikit-image`
- **Cloud & Networking**: `grpcio` & `grpcio-tools`, `apache-airflow`, `sagemaker`, various Azure packages (`azure-identity`, `azure-storage-blob`, `azure-cli`), various Snowflake packages (`snowflake-connector-python`, `snowflake-sqlalchemy`)
- **XML / File parsing**: `lxml` (Installation/Build barriers), `ruamel-yaml`, `h5py`
- **Build / Packaging**: `poetry` & `poetry-plugin-export`
- **Auth**: `msal` & `msal-extensions`
- **Jupyter Stack**: `jupyterlab`, `jupyter-server`, `notebook`

*(Note: Most pure-Python libraries continue to work fine, provided their underlying C-extension dependencies are updated. Packages heavily relying on Cython or Rust's PyO3 often require upstream updates before they can claim free-threading compatibility.)*

*(Check `incompatible_packages.txt` for the full list of 64 top-tier failing packages.)*

---

## 🐛 Known Standard Library & CPython Limitations

Even within the reference CPython implementation, the migration to free-threading has exposed race conditions and limitations that are actively being patched on the issue tracker:

- **Data Races in Standard Modules**: Ongoing issues have been logged for data races in `_tkinter.c` (on `event_tstate`), GC debug flags (`gc.set_debug`/`get_debug`), stateful codecs (`codecctx_errors_set`), `itertools` (concurrent iteration on `itertools.tee` and `itertools.islice`), `FileIO`, and `string.Template` compilation.
- **Reference Counting & Memory Errors**: Issues like use-after-free when reading `sys._current_frames()`, segfaults during `os.scandir` iteration, and race conditions during concurrent accesses to `sys._current_exceptions()` or shared `BytesIO` buffers.
- **Opcode Safety**: Opcodes like `LIST_APPEND` and `SET_ADD` are being evaluated for thread safety under free-threading.

As the ecosystem adapts to PEP 703, these libraries will gradually gain thread-safe C-extension binaries (wheels) for Python 3.13+. It is currently recommended that complex multi-threaded applications thoroughly audit and test all dependencies before deploying the free-threaded build to production.

---

## 🛠️ Actionable Contribution Angles

You can directly accelerate the ecosystem's journey toward true parallelism in Python. Jump in, pick a library, and help build the future of Python!

### 1. The "Ecosystem CI" Angle (Safe & High Impact)
Thousands of open-source projects haven't even tested if they work without the GIL yet. Add Python `3.13t` and `3.14t` (the free-threaded builds) to their GitHub Actions / CI testing matrices.
👉 *Check out the `ecosystem_ci/` directory in this repo for a real example of how to stage this for a popular library (`PyGithub`).*

### 2. The "Pure Python Implicit State" Angle
Without the GIL, pure Python code that shares global mutable state across threads might experience race conditions. Audit pure Python libraries for global variables, class-level mutable attributes, or cached singletons, and submit PRs wrapping these in explicit `threading.Lock()`.

### 3. The "C-Extension Modernization" Angle
Help migrate C extensions to use **PEP 489 (Multi-phase extension module initialization)**, moving static C variables into a struct tied to the module instance, and applying the `Py_mod_gil` slot to tell Python 3.13+ to keep the GIL disabled.

### 4. Cython / PyO3 Migration
Test and update Rust-backed Python packages with PyO3's new `gil-refs` disabled features, or update projects to Cython 3.1+ (which adds free-threading compatibility).

### 5. ThreadSanitizer (TSAN) Bug Hunting
Compile CPython or a major library with TSAN enabled (`./configure --with-thread-sanitizer`). Run the test suite and report data races to the core developers.
