import os
import functools
import tempfile


def run_in_tmpdir(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            f(*args, **kwargs)
    return inner

