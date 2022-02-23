
import os
import tempfile


def run_in_tmpdir(f):
    def inner():
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            f()
    return inner

