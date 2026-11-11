# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyXDG: pure-Python implementations of freedesktop.org specs (basedir, desktop entry, menu, icon theme, shared MIME-info, recent files). No runtime dependencies. Supports Python 3.10 to 3.15 (`python_requires=">=3.10"`, CI matrix in `.github/workflows/test.yml`). `xdg/util.py` (`PY3`, `u()`, `which`) is a deprecated shim kept only for external callers; don't use it internally.

This is the Xpra-org fork (`origin`); the original project is `upstream` (takluyver/pyxdg).

## Commands

```sh
pytest                                   # run the whole suite (what CI runs)
pytest test/test_menu.py                 # one file
pytest test/test_menu.py::MenuTest::test_parse_menu   # one test
make -C docs html                        # Sphinx docs (docs/*.rst, published on RTD)
```

There is no linter configuration.

pytest is configured in `pyproject.toml`. Its `pythonpath = ["."]` makes tests import the local `xdg/` package rather than a system-installed pyxdg. It also disables the `pytest-relaxed` plugin, because that plugin would collect the standalone scripts `test/fuzz-mime.py` and `test/menu-spec/`, which are not pytest tests.

`xdg/Menu.py` compiles menu `<Include>`/`<Exclude>` rules into Python ASTs. Build nodes with `ast.Constant` and pass required fields to the constructors (`ast.Expression(body=...)`); Python 3.15 rejects missing or unknown constructor arguments.

## Architecture

All code lives in the flat `xdg/` package, one module per spec:

- `BaseDirectory` is the foundation. It reads `XDG_*` environment variables **once at import time** into module-level globals (`xdg_data_dirs`, `xdg_config_dirs`, and so on). Other modules import those values (`from xdg.BaseDirectory import xdg_data_dirs`), so they also capture them at import time.
- `IniFile` is the shared parser and validator for the INI-style formats. `DesktopEntry` and `IconTheme`/`IconData` subclass it and add spec-specific keys and validation. Localized keys (`Name[de]`) are resolved through `xdg.Locale.langs`.
- `Menu` parses `.menu` XML (`XMLMenuBuilder`), applies include/exclude rules (`Rule` compiles to Python AST), merges directories, and builds a `Menu` tree of `MenuEntry` objects backed by `DesktopEntry`. `MenuEditor` sits on top of it to write user overrides.
- `Mime` loads the shared MIME database (globs, magic, aliases, subclasses) lazily into module-level caches (`update_cache()`).
- `Config` holds global settings (locale, icon theme and size, cache time, root mode) as module globals that other modules read.
- `Exceptions` defines the error hierarchy (`ParsingError`, `ValidationError`, `NoKeyError`, ...) that the parsers raise.

Because so much state is module-level and fixed at import time, tests that change the environment must set `os.environ` and then `reload()` the affected modules (and their dependents, for example `BaseDirectory` then `DesktopEntry` then `Menu`). See `test/test_basedirectory.py` for the pattern of saving and restoring `environ`. Test fixture file contents (desktop files, menus, icons) live as strings in `test/resources.py`, and tests write them to temp dirs.

## Release notes

When bumping the version, update `setup.py`, `xdg/__init__.py` (`__version__`), and `ChangeLog` together. They are currently out of sync: `setup.py` is at 0.29, `__init__.py` at 0.28.
