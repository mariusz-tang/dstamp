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

## Contributing

If you'd like to see something added to dstamp or if you would like to add something
yourself, please see [CONTRIBUTING](./CONTRIBUTING.md)!

Please also see the above if you have a bug to report.
