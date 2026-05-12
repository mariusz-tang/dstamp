"""Fixtures for the functional tests."""

import pytest
from pytest_mock import MockerFixture

from dstamp import config, main


@pytest.fixture(autouse=True)
def config_path(mocker: MockerFixture, tmp_path):
    """
    Change the default config location so that it is empty for tests.

    Returns the new default config location.
    """

    get_config_path = mocker.patch("dstamp.config.platformdirs.user_config_path")
    get_config_path.return_value = tmp_path
    return config.get_config_path()


@pytest.fixture(autouse=True)
def disable_clipboard(mocker: MockerFixture):
    """Disable clipboard interactions so tests can be run on CI."""
    mocker.patch("dstamp.main.pyperclip.copy")


@pytest.fixture(autouse=True)
def disable_color_output(mocker: MockerFixture):
    """Disable colour output so the captured output is in plaintext."""
    mocker.patch("dstamp.console.info", print)
    mocker.patch("dstamp.console.warn", print)
    mocker.patch("dstamp.console.error", print)


@pytest.fixture
def app(capsys):
    """Return an app runner."""

    def run(*args):
        error_code = main.app.meta(args, result_action="return_value")
        output = capsys.readouterr().out
        return error_code, output

    return run
