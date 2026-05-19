# dstamp

CLI app for generating timestamps for use in Discord chats.

*Note*: This is a complete rewrite of the original project from the ground up,
using the standard argparse module instead of cyclopts.

## TODO

At this stage, the priority is to achieve feature-parity with v2:

- Add error handling.
- Add date and time keywords like "midnight" and "tomorrow".
- Add copy to clipboard.
- Add rounding.
- Add version flag.
- Add shell completion.
- Add config file support.
- Add show-config.

## Installation

Install using [pipx] or [uv]:

```bash
pipx install dstamp
```

```bash
uv tool install dstamp
```

[pipx]: https://pipx.pypa.io/stable/
[uv]: https://docs.astral.sh/uv/

## Versioning

This project uses an `MAJOR.MINOR` versioning scheme. `MAJOR` is incremented for
significant feature additions or changes. Everything else increments `MINOR`
only. `MINOR` is omitted if it is zero.

## Contributing

If you'd like to see something added to dstamp or if you would like to add something
yourself, please see [CONTRIBUTING](./CONTRIBUTING.md)!

Please also see the above if you have a bug to report.
