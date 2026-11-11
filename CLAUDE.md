# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyXDG: pure-Python implementations of freedesktop.org specs (basedir, desktop entry, menu, icon theme, shared MIME-info, recent files). No runtime dependencies. Python 3 only (`python_requires=">=3.2"`; Python 2 support was dropped in 0.29, though some `PY3` / `u()` compatibility shims in `xdg/util.py` remain).

This is the Xpra-org fork (`origin`); the original project is `upstream` (takluyver/pyxdg).

## Commands

```sh
pytest                                   # run the whole suite (what CI runs)
pytest test/test_menu.py                 # one file
pytest test/test_menu.py::MenuTest::test_parse_menu   # one test
make -C docs html                        # Sphinx docs (docs/*.rst, published on RTD)
```

There is no linter configuration.

The repo has no pytest config of its own. On this machine, pytest walks up and picks `~/pyproject.toml` (an unrelated Pillow config) as its config file, so bare `pytest` breaks during collection (it imports `setup.py`). Run the suite in isolation:

```sh
python -m pytest --rootdir=. -c /dev/null test/test_*.py
```

`test/fuzz-mime.py` and `test/menu-spec/` are standalone scripts, not pytest tests.

Known breakage on Python 3.12+ (CI only tests up to 3.10):
- `test/test_basedirectory.py` falls back to `from imp import reload`. The `imp` module was removed in 3.12; use `importlib.reload`.
- `xdg/Menu.py` builds rule ASTs with `ast.Str` (removed in 3.12), so menu parsing and `Rule` compilation raise `AttributeError`. Use `ast.Constant`.

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
