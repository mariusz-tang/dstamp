"""unit/test_format.py

This module contains unit tests for the dstamp.format module.
"""

import datetime

import pytest

from dstamp import format
from tests.utils.parse import Timestamp


@pytest.mark.parametrize("form", (form for form in format.Format))
def test_convert_to_discord_format(form: format.Format):
    dt = datetime.datetime.now()
    formatted_time = format.convert_to_discord_format(dt, form)
    stamp = Timestamp(formatted_time)
    assert stamp.format_code == form.code
    assert stamp.timestamp == int(dt.timestamp())
