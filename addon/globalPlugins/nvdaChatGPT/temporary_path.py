import sys
import os
from contextlib import contextmanager


@contextmanager
def temporary_sys_path():
    original_sys_path = sys.path.copy()
    package_path = os.path.join(os.path.dirname(__file__), "site-packages")
    sys.path.insert(0, package_path)
    try:
        yield
    finally:
        sys.path = original_sys_path
