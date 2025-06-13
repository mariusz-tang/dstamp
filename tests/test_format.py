import datetime

import pytest

from dstamp import format
from tests.timestamp import Timestamp


@pytest.mark.parametrize("form", (form for form in format.Format))
def test_format(form: format.Format):
    dt = datetime.datetime.now()
    formatted_time = format.convert_to_discord_format(dt, form)
    stamp = Timestamp(formatted_time)
    assert stamp.format_code == form.code
    assert stamp.timestamp == str(int(dt.timestamp()))
