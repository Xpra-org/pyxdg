"""
Deprecated Python 2 compatibility helpers, kept so that existing
imports keep working. Do not use in new code.
"""
from shutil import which  # noqa: F401

PY3 = True


def u(s):
    return s
