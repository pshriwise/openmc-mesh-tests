import pytest

from pincell import config as pincell_config


def pytest_addoption(parser):
    parser.addoption('--exe')
    parser.addoption('--build-inputs', action='store_true')


def pytest_configure(config):
    opts = ['exe', 'build_inputs']
    for opt in opts:
        if config.getoption(opt) is not None:
            pincell_config[opt] = config.getoption(opt)


@pytest.fixture
def run_in_tmpdir(tmpdir):
    orig = tmpdir.chdir()
    try:
        yield
    finally:
        orig.chdir()
