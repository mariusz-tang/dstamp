import pathlib

import pytest

from dstamp import config


def test_default_path(config_path: pathlib.Path) -> None:
    assert config.default_path() == config_path


@pytest.mark.parametrize(
    "cfg",
    [
        {"copy": True},
        {"copy": False},
        {"format": "short-time"},
        {"precision": "20s"},
        {"copy": True, "format": "long-time", "precision": "60s"},
        {"quiet": True},
        {"verbose": False, "quiet": True},
    ],
)
def test_clean_valid_keys_only(cfg: dict) -> None:
    assert config.clean(cfg) == (cfg, set())


@pytest.mark.parametrize(
    "cfg",
    [
        {"cop": True},
        {"cpy": False},
        {"frmat": "short-time"},
        {"prcision": "20s"},
        {"coy": True, "formt": "long-time", "prcision": "60s"},
        {"quet": True},
        {"vrbose": False, "uiet": True},
    ],
)
def test_clean_invalid_keys_only(cfg: dict) -> None:
    assert config.clean(cfg) == ({}, cfg.keys())


@pytest.mark.parametrize(
    ("cfg", "cleaned", "invalid_keys"),
    [
        (
            {"coy": True, "format": "long-time", "precision": "60s"},
            {"format": "long-time", "precision": "60s"},
            {"coy"},
        ),
        ({"vrbose": False, "quiet": True}, {"quiet": True}, {"vrbose"}),
    ],
)
def test_clean_valid_and_invalid_keys(
    cfg: dict, cleaned: dict, invalid_keys: set
) -> None:
    assert config.clean(cfg) == (cleaned, invalid_keys)
