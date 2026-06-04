import pathlib
import unittest.mock

import pytest
import pytest_mock


@pytest.fixture(autouse=True)
def config_path(
    tmp_path: pathlib.Path, mocker: pytest_mock.MockerFixture
) -> pathlib.Path:
    """Use a temporary directory for the config path during tests."""
    mocker.patch("dstamp.config.platformdirs.user_config_path").return_value = tmp_path
    return tmp_path / "config.toml"


@pytest.fixture(autouse=True)
def logging_config_mock(mocker: pytest_mock.MockerFixture) -> unittest.mock.Mock:
    """Do not configure logging so that the logassert fixture can do it.

    This also stops the logfile from being cluttered by logs emitted during
    tests.

    Returns the patched configuration function.
    """
    return mocker.patch("dstamp.cli.logging.config.dictConfig")
