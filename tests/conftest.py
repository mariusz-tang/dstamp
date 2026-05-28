import pathlib

import pytest
import pytest_mock


@pytest.fixture(autouse=True)
def config_path(
    tmp_path: pathlib.Path, mocker: pytest_mock.MockerFixture
) -> pathlib.Path:
    mocker.patch("platformdirs.user_config_path").return_value = tmp_path
    return tmp_path / "config.toml"
