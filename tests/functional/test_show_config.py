"""functional/test_show_config.py

This module contains functional tests for the dstamp show-config command.
"""

from dstamp import format
from tests.utils import config, dstamp_cli


def test_no_parameters(empty_default_config):
    output = dstamp_cli.run_show_config()
    assert output.config_path == empty_default_config
    assert not output.has_using_default_warning
    assert output.copy_to_clipboard is False
    assert output.output_format == format.Format.RELATIVE.value


def test_invalid_toml():
    output = dstamp_cli.run_show_config(str(config.INVALID_TOML_PATH))
    assert output.config_path == config.INVALID_TOML_PATH
    assert output.has_using_default_warning
    assert output.invalid_toml
    assert not output.not_a_file


def test_copy_config():
    output = dstamp_cli.run_show_config(str(config.COPY_CONFIG_PATH))
    assert output.config_path == config.COPY_CONFIG_PATH
    assert output.copy_to_clipboard is True


def test_format_config():
    output = dstamp_cli.run_show_config(str(config.SHORT_TIME_FORMAT_CONFIG_PATH))
    assert output.config_path == config.SHORT_TIME_FORMAT_CONFIG_PATH
    assert output.output_format == format.Format.SHORT_TIME.value
