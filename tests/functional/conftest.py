"""Fixtures for the functional tests."""

import pytest

from dstamp import config, console, main


@pytest.fixture(autouse=True)
def config_path(monkeypatch, tmp_path):
    """
    Change the default config location so that it is empty for tests.

    Returns the new default config location.
    """
    monkeypatch.setattr(
        config.platformdirs, "user_config_path", lambda *_, **__: tmp_path
    )
    return config.get_config_path()


@pytest.fixture(autouse=True)
def disable_clipboard(monkeypatch):
    """Disable clipboard interactions so tests can be run on CI."""

    def do_nothing(*_):
        pass

    monkeypatch.setattr(main.pyperclip, "copy", do_nothing)


@pytest.fixture(autouse=True)
def disable_color_output(monkeypatch):
    """Disable colour output so the captured output is in plaintext."""
    monkeypatch.setattr(console, "info", print)
    monkeypatch.setattr(console, "warn", print)
    monkeypatch.setattr(console, "error", print)


@pytest.fixture
def app(capsys):
    """Return an app runner."""

    def run(*args):
        error_code = main.app.meta(args, result_action="return_value")
        output = capsys.readouterr().out
        return error_code, output

    return run
