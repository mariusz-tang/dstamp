# dstamp

CLI app for generating timestamps for use in Discord chats.

## TODO

I intend to rewrite this project to use the standard argparse library instead
of cyclopts. This makes the whole typer-to-cyclopts migration seem rather silly.
My reasoning is that cyclopts is a bit too heavy-handed for my tastes, and I
prefer how argparse forces you to separate parsing from handling functions.

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

dstamp accepts a TOML configuration file which can override any command-line
argument. Keys should be structured as `command.option`. For example, to enable
rounding by default and set a custom default rounding precision for the `get`
command, you could do the following:

```toml
[get]
round = true
precision = "15m"
```

Use the `show-config` command to find the default config location. Specify the
`--config` flag to use a different file.

```bash
dstamp show-config
dstamp --config ./path-to-a-different-file.toml
```

## Versioning

This project uses an `X.Y` versioning scheme. Bugfixes will move the version to
`X.Y+1`, and anything else will move it to `X+1.0`. If `Y` is 0, we omit it,
so `X+1.0` actually just becomes `X+1`.

## Contributing

If you'd like to see something added to dstamp or if you would like to add something
yourself, please see [CONTRIBUTING](./CONTRIBUTING.md)!

Please also see the above if you have a bug to report.
