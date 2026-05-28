import pathlib

import pytest
import pytest_mock

from dstamp import config


@pytest.fixture(autouse=True)
def config_path(
    tmp_path: pathlib.Path, mocker: pytest_mock.MockerFixture
) -> pathlib.Path:
    mocker.patch("platformdirs.user_config_path").return_value = tmp_path
    return tmp_path / "config.toml"


def test_default_path(config_path: pathlib.Path) -> None:
    assert config.default_path() == config_path


def test_parse_non_existent_file_returns_empty(config_path: pathlib.Path) -> None:
    assert config.parse(config_path) == {}


def test_parse_empty_file_returns_empty(config_path: pathlib.Path) -> None:
    config_path.touch()
    assert config.parse(config_path) == {}


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
    assert config.parse(config_path) == expected_result


def test_parse_unrecognized_keys_triggers_warning(config_path: pathlib.Path) -> None:
    config_path.write_text("copy=true\nunknown_key='hello!'\nanother='byeee'")

    with pytest.warns(UserWarning, match="unknown keys in config file") as record:
        config.parse(config_path)

    assert len(record) == 1
    message = str(record[0].message)
    assert "unknown_key" in message
    assert "another" in message
    assert "copy" not in message
