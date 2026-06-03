import pathlib

import pytest
import pytest_mock


@pytest.fixture(autouse=True)
def config_path(
    tmp_path: pathlib.Path, mocker: pytest_mock.MockerFixture
) -> pathlib.Path:
    """Use a temporary directory for the config path during tests."""
    mocker.patch("dstamp.config.platformdirs.user_config_path").return_value = tmp_path
    return tmp_path / "config.toml"
