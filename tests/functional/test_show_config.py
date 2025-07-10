"""functional/test_show_config.py

This module contains functional tests for the dstamp show-config command.
"""

from tests.utils import dstamp_cli


def test_no_parameters(empty_default_config):
    output = dstamp_cli.run_show_config()
    assert output.config_path == empty_default_config
