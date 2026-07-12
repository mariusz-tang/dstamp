from dstamp import logging


def test_get_config_normal() -> None:
    assert logging.get_config("normal") == logging.CONFIG


def test_get_config_quiet() -> None:
    assert "console" in logging.get_config("normal")["root"]["handlers"]
    assert "console" not in logging.get_config("quiet")["root"]["handlers"]


def test_get_config_verbose() -> None:
    assert logging.get_config("normal")["handlers"]["console"]["level"] == "WARNING"
    assert logging.get_config("verbose")["handlers"]["console"]["level"] == "INFO"
