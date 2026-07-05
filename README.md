# Incompatible Libraries and Limitations with Python Free-Threading (No-GIL)

Python 3.13 introduced an experimental no-GIL (free-threaded) build, with further documented support arriving in Python 3.14. Because this paradigm shifts how thread safety is handled (removing the Global Interpreter Lock), many existing C extensions, third-party libraries, and even standard library modules face race conditions or incompatibilities until they are updated.

## Notable Incompatible Libraries
Based on active compatibility tracking (from sources like `parallel.python.tips` and `py-free-threading`), several prominent libraries currently report issues or lack full support for the free-threaded build. In some cases, the installation or import fails outright because the library enforces GIL-only constraints, or they experience significant data races:

- **cryptography** (Installs, but fails to import without the GIL)
- **cffi** (Fails during install/import in free-threading mode)
- **pydantic-core** (Installs, but fails to import without the GIL)
- **grpcio** & **grpcio-tools** (Installation/Build barriers)
- **lxml** (Installation/Build barriers)
- **tensorflow** (Installation/Build barriers)
- **pyopenssl**
- **pynacl**
- **poetry** & **poetry-plugin-export**
- **snowflake-connector-python** & **snowflake-sqlalchemy**
- **msal** & **msal-extensions**
- **azure-identity**, **azure-storage-blob**, **azure-cli**
- **apache-airflow**
- **sagemaker**
- **jupyterlab**, **jupyter-server**, **notebook**

*(Note: Most pure-Python libraries continue to work fine, provided their underlying C-extension dependencies are updated. Packages heavily relying on Cython or Rust's PyO3 often require upstream updates before they can claim free-threading compatibility.)*

## Standard Library & CPython Limitations
Even within the reference CPython implementation, the migration to free-threading has exposed race conditions and limitations that are actively being patched on the issue tracker:

- **Data Races in Standard Modules**: Ongoing issues have been logged for data races in `_tkinter.c`, GC debug flags, stateful codecs (`codecctx_errors_set`), `itertools.tee` concurrent iteration, and `string.Template` compilation.
- **Reference Counting & Memory Errors**: Issues like use-after-free when reading `sys._current_frames()`, segfaults during `os.scandir` iteration, and race conditions during concurrent accesses to `sys._current_exceptions()` or shared `BytesIO` buffers.
- **Opcode Safety**: Opcodes like `LIST_APPEND` and `SET_ADD` are being evaluated for thread safety under free-threading.

As the ecosystem adapts to PEP 703, these libraries will gradually gain thread-safe C-extension binaries (wheels) for Python 3.13+. It is currently recommended that complex multi-threaded applications thoroughly audit and test all dependencies before deploying the free-threaded build to production.
