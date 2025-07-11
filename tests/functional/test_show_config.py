"""functional/test_show_config.py

This module contains functional tests for the dstamp show-config command.
"""

from dstamp import format
from tests.utils import dstamp_cli
from tests.utils.config import INVALID_TOML_PATH


def test_no_parameters(empty_default_config):
    output = dstamp_cli.run_show_config()
    assert output.config_path == empty_default_config
    assert not output.has_using_default_warning
    assert output.copy_to_clipboard is False
    assert output.output_format == format.Format.RELATIVE.value


def test_invalid_toml():
    output = dstamp_cli.run_show_config(str(INVALID_TOML_PATH))
    assert output.config_path == INVALID_TOML_PATH
    assert output.has_using_default_warning
    assert output.invalid_toml
    assert not output.not_a_file
