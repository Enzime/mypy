from __future__ import print_function
"""This file is used to find the site packages of a Python executable, which may be Python 2.

This file MUST remain compatible with Python 2. Since we cannot make any assumptions about the
Python being executed, this module should not use *any* dependencies outside of the standard
library found in Python 2. This file is run each mypy run, so it should be kept as fast as
possible.
"""

import sys
import os
import site
import sysconfig

if __name__ == '__main__':
    sys.path = sys.path[1:]  # we don't want to pick up mypy.types

MYPY = False
if MYPY:
    from typing import List, Tuple


def getsearchdirs():
    # type: () -> Tuple[List[str], List[str]]
    site_packages = _getsitepackages()

    # Do not include things from the standard library
    # because those should come from typeshed.
    stdlib_zip = os.path.join(
        sys.base_exec_prefix,
        getattr(sys, "platlibdir", "lib"),
        "python{}{}.zip".format(sys.version_info.major, sys.version_info.minor)
    )
    stdlib = sysconfig.get_path("stdlib")
    stdlib_ext = os.path.join(stdlib, "lib-dynload")
    cwd = os.path.abspath(os.getcwd())
    excludes = set(site_packages + [cwd, stdlib_zip, stdlib, stdlib_ext])

    abs_sys_path = (os.path.abspath(p) for p in sys.path)
    return (site_packages, [p for p in abs_sys_path if p not in excludes])


def _getsitepackages():
    # type: () -> List[str]
    if hasattr(site, 'getusersitepackages') and hasattr(site, 'getsitepackages'):
        user_dir = site.getusersitepackages()
        return site.getsitepackages() + [user_dir]
    else:
        from distutils.sysconfig import get_python_lib
        return [get_python_lib()]


if __name__ == '__main__':
    print(repr(getsearchdirs()))
