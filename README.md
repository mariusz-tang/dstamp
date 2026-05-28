# dstamp

CLI app for generating timestamps for use in Discord chats.

*Note*: This is a complete rewrite of the original project from the ground up,
using the standard argparse module instead of cyclopts.

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

## Usage

```bash
# Get the current time.
dstamp get

# Get the current time, to the nearest 15 minutes.
dstamp get --precision 15m

# Show the config file location.
dstamp show-config
```

See the help messages for full usage information:

```bash
dstamp -h
dstamp -h get
```

### Configuration

Dstamp supports configuration by TOML file. See `dstamp -h show-config` for full
information.

## Shell completion

Dstamp supports shell completion using [argcomplete]. See the argcomplete
documentation for setup instructions.

[argcomplete]: https://github.com/kislyuk/argcomplete#activating-global-completion

## Versioning

This project uses an `MAJOR.MINOR` versioning scheme. `MAJOR` is incremented for
significant feature additions or changes. Everything else increments `MINOR`
only. `MINOR` is omitted if it is zero.

## Contributing

If you'd like to see something added to dstamp or if you would like to add something
yourself, please see [CONTRIBUTING](./CONTRIBUTING.md)!

Please also see the above if you have a bug to report.
