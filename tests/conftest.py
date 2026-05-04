import clipman
import pytest

from dstamp import config
from tests.utils.config import EMPTY_CONFIG_PATH


@pytest.fixture(autouse=True)
def empty_default_config(monkeypatch):
    """
    Change the default config location so that it is empty for tests.

    Returns the new default config location.
    """
    monkeypatch.setattr(config, "get_config_path", lambda: EMPTY_CONFIG_PATH)
    return EMPTY_CONFIG_PATH


@pytest.fixture(autouse=True)
def disable_clipboard(monkeypatch):
    """Disable clipboard interactions so tests can be run on CI."""

    def do_nothing(*_):
        pass

    monkeypatch.setattr(clipman, "init", do_nothing)
    monkeypatch.setattr(clipman, "set", do_nothing)
