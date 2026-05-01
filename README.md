# dstamp

CLI app for generating timestamps for use in Discord chats.

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

## Example usage

```bash
# For the current time
dstamp get

# Two hours in the future
dstamp get --offset 2h

# Round to the nearest hour
dstamp get --offset 2h --round --precision h

# Copy to clipboard
dstamp --copy-to-clipboard
```

For full documentation see the help messages:

```bash
dstamp --help
dstamp get --help
```

## Configuration

TODO

## Contributing

If you'd like to see something added to dstamp or if you would like to add something
yourself, please see [CONTRIBUTING](./CONTRIBUTING.md)!

Please also see the above if you have a bug to report.
