from pathlib import Path

from tests.typing import AppRunner


def test_show_config(app: AppRunner[str], config_path: Path) -> None:
    error_code, output = app("show-config")
    assert error_code == 0
    assert output.strip() == str(config_path)
