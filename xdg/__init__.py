"""PyXDG: implementations of freedesktop.org standards.

The functions in this module return the XDG base directories as
:class:`pathlib.Path` objects, with the same API as the ``xdg`` package
from https://github.com/srstevenson/xdg. Unlike the module-level values in
:mod:`xdg.BaseDirectory`, they read the environment each time they are called.
"""

import os
from pathlib import Path

__all__ = [
    "BaseDirectory",
    "DesktopEntry",
    "Menu",
    "Exceptions",
    "IniFile",
    "IconTheme",
    "Locale",
    "Config",
    "Mime",
    "RecentFiles",
    "MenuEditor",
    "xdg_cache_home",
    "xdg_config_dirs",
    "xdg_config_home",
    "xdg_data_dirs",
    "xdg_data_home",
    "xdg_runtime_dir",
    "xdg_state_home",
]

__version__ = "0.29"


# The spec says that empty variables are treated as unset, and that relative
# paths are invalid and must be ignored.

def _path_from_env(variable: str, default: Path) -> Path:
    value = os.environ.get(variable)
    if value and os.path.isabs(value):
        return Path(value)
    return default


def _paths_from_env(variable: str, default: list[Path]) -> list[Path]:
    value = os.environ.get(variable)
    if value:
        paths = [Path(path) for path in value.split(os.pathsep) if os.path.isabs(path)]
        if paths:
            return paths
    return default


def xdg_cache_home() -> Path:
    """Return a Path corresponding to XDG_CACHE_HOME."""
    return _path_from_env("XDG_CACHE_HOME", Path.home() / ".cache")


def xdg_config_dirs() -> list[Path]:
    """Return a list of Paths corresponding to XDG_CONFIG_DIRS.

    Unlike :data:`xdg.BaseDirectory.xdg_config_dirs`, this does not include
    XDG_CONFIG_HOME.
    """
    return _paths_from_env("XDG_CONFIG_DIRS", [Path("/etc/xdg")])


def xdg_config_home() -> Path:
    """Return a Path corresponding to XDG_CONFIG_HOME."""
    return _path_from_env("XDG_CONFIG_HOME", Path.home() / ".config")


def xdg_data_dirs() -> list[Path]:
    """Return a list of Paths corresponding to XDG_DATA_DIRS.

    Unlike :data:`xdg.BaseDirectory.xdg_data_dirs`, this does not include
    XDG_DATA_HOME.
    """
    return _paths_from_env(
        "XDG_DATA_DIRS", [Path("/usr/local/share"), Path("/usr/share")]
    )


def xdg_data_home() -> Path:
    """Return a Path corresponding to XDG_DATA_HOME."""
    return _path_from_env("XDG_DATA_HOME", Path.home() / ".local" / "share")


def xdg_runtime_dir() -> Path | None:
    """Return a Path corresponding to XDG_RUNTIME_DIR.

    If the XDG_RUNTIME_DIR environment variable is not set (or is empty or
    relative), None is returned, as the specification defines no default.
    Use :func:`xdg.BaseDirectory.get_runtime_dir` for a fallback directory.
    """
    value = os.environ.get("XDG_RUNTIME_DIR")
    if value and os.path.isabs(value):
        return Path(value)
    return None


def xdg_state_home() -> Path:
    """Return a Path corresponding to XDG_STATE_HOME."""
    return _path_from_env("XDG_STATE_HOME", Path.home() / ".local" / "state")
