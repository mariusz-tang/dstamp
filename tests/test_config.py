import pathlib

import pytest

from dstamp import config


def test_default_path(config_path: pathlib.Path) -> None:
    assert config.default_path() == config_path


def test_parse_non_existent_file_returns_empty(config_path: pathlib.Path) -> None:
    assert config.parse(config_path) == ({}, set())


def test_parse_empty_file_returns_empty(config_path: pathlib.Path) -> None:
    config_path.touch()
    assert config.parse(config_path) == ({}, set())


@pytest.mark.parametrize(
    ("config_text", "expected_result"),
    [
        ("copy = true", {"copy": True}),
        ("copy = false", {"copy": False}),
        ("format = 'short-time'", {"format": "short-time"}),
        ("precision = '20s'", {"precision": "20s"}),
        (
            "copy=true\nformat='long-time'\nprecision='60s'",
            {"copy": True, "format": "long-time", "precision": "60s"},
        ),
    ],
)
def test_parse_valid_options(
    config_path: pathlib.Path, config_text: str, expected_result: dict
) -> None:
    config_path.write_text(config_text)
    assert config.parse(config_path) == (expected_result, set())


def test_parse_no_args_uses_default_config_path(config_path: pathlib.Path) -> None:
    config_path.write_text("copy=true")
    assert config.parse() == ({"copy": True}, set())


def test_parse_unrecognized_keys_are_returned_in_second_part(
    config_path: pathlib.Path,
) -> None:
    config_path.write_text("copy=true\nunknown_key='hello!'\nanother='byeee'")

    assert config.parse(config_path) == ({"copy": True}, {"unknown_key", "another"})
