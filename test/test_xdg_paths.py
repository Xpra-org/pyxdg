"""Tests for the pathlib-based base directory functions in xdg/__init__.py."""

import os
import unittest
from os import environ
from pathlib import Path

import xdg

HOME_FUNCTIONS = {
    "XDG_CACHE_HOME": (xdg.xdg_cache_home, Path.home() / ".cache"),
    "XDG_CONFIG_HOME": (xdg.xdg_config_home, Path.home() / ".config"),
    "XDG_DATA_HOME": (xdg.xdg_data_home, Path.home() / ".local" / "share"),
    "XDG_STATE_HOME": (xdg.xdg_state_home, Path.home() / ".local" / "state"),
}

DIRS_FUNCTIONS = {
    "XDG_CONFIG_DIRS": (xdg.xdg_config_dirs, [Path("/etc/xdg")]),
    "XDG_DATA_DIRS": (xdg.xdg_data_dirs, [Path("/usr/local/share"), Path("/usr/share")]),
}


class XdgPathsTest(unittest.TestCase):
    def setUp(self):
        self.environ_save = environ.copy()

    def tearDown(self):
        environ.clear()
        environ.update(self.environ_save)

    def test_home_set(self):
        for var, (func, _default) in HOME_FUNCTIONS.items():
            with self.subTest(var=var):
                environ[var] = "/some/where"
                self.assertEqual(func(), Path("/some/where"))

    def test_home_default(self):
        for var, (func, default) in HOME_FUNCTIONS.items():
            for value in (None, "", "relative/path"):
                with self.subTest(var=var, value=value):
                    environ.pop(var, None)
                    if value is not None:
                        environ[var] = value
                    self.assertEqual(func(), default)

    def test_home_reads_environment_at_call_time(self):
        environ["XDG_CONFIG_HOME"] = "/first"
        self.assertEqual(xdg.xdg_config_home(), Path("/first"))
        environ["XDG_CONFIG_HOME"] = "/second"
        self.assertEqual(xdg.xdg_config_home(), Path("/second"))

    def test_dirs_set(self):
        for var, (func, _default) in DIRS_FUNCTIONS.items():
            with self.subTest(var=var):
                environ[var] = os.pathsep.join(["/a", "relative", "", "/b"])
                self.assertEqual(func(), [Path("/a"), Path("/b")])

    def test_dirs_default(self):
        for var, (func, default) in DIRS_FUNCTIONS.items():
            for value in (None, "", "relative:also/relative"):
                with self.subTest(var=var, value=value):
                    environ.pop(var, None)
                    if value is not None:
                        environ[var] = value
                    self.assertEqual(func(), default)

    def test_runtime_dir(self):
        environ["XDG_RUNTIME_DIR"] = "/run/user/1234"
        self.assertEqual(xdg.xdg_runtime_dir(), Path("/run/user/1234"))
        for value in (None, "", "relative"):
            with self.subTest(value=value):
                environ.pop("XDG_RUNTIME_DIR", None)
                if value is not None:
                    environ["XDG_RUNTIME_DIR"] = value
                self.assertIsNone(xdg.xdg_runtime_dir())

    def test_all_exports_exist(self):
        for name in xdg.__all__:
            if name.startswith("xdg_"):
                self.assertTrue(callable(getattr(xdg, name)), name)
