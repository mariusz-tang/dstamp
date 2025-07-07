import pytest

from dstamp.format import Format
from tests.utils.parse import Timestamp


@pytest.mark.parametrize(
    "format_str", ("{}", "gjaifejf{}aiojoiajfe", "\n\naiojda\n{}\n\n\n")
)
def test_timestamp_ignores_extra_text(format_str: str):
    timestamp = 1749682800
    code = Format.RELATIVE.code
    text = str.format(format_str, f"<t:{timestamp}:{code}>")
    stamp = Timestamp(text)
    assert stamp.timestamp == timestamp
    assert stamp.format_code == code


@pytest.mark.parametrize(
    "format_str",
    ("{}{}", "awadad{}awdad{}wad", "daopdka\naoip\n{}jaioj\nas{}aosdaks\n\n"),
)
def test_timestamp_grabs_first_match(format_str: str):
    timestamps = 4921319031, 123913202
    codes = Format.RELATIVE.code, Format.SHORT_DATE.code

    text = str.format(
        format_str, f"<t:{timestamps[0]}:{codes[0]}>", f"<t:{timestamps[1]}:{codes[1]}>"
    )
    stamp = Timestamp(text)
    assert stamp.timestamp == timestamps[0]
    assert stamp.format_code == codes[0]

    text_reversed = str.format(
        format_str, f"<t:{timestamps[1]}:{codes[1]}>", f"<t:{timestamps[0]}:{codes[0]}>"
    )
    stamp_reversed = Timestamp(text_reversed)
    assert stamp_reversed.timestamp == timestamps[1]
    assert stamp_reversed.format_code == codes[1]


@pytest.mark.parametrize("text", ("", "aekfafk", "\n\n\nowajaoi\n"))
def test_timestamp_errors_on_no_match(text: str):
    with pytest.raises(ValueError):
        Timestamp(text)
