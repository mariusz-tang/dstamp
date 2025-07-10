from pathlib import Path

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
