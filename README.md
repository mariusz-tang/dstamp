# dstamp

CLI app for generating timestamps for use in Discord chats.

## Example usage

```bash
# For the current time
dstamp get

# Two hours in the future
dstamp get --offset 2h

# Round to the nearest hour
dstamp get -o 2h --round --precision h

# Copy to clipboard
dstamp --copy-to-clipboard

# Show active configuration
dstamp show-config
```

For full documentation see the help messages:

```bash
dstamp --help
dstamp get --help
dstamp show-config --help
```

## Contributing

If you'd like to see something added to dstamp or if you would like to add something
yourself, please see [CONTRIBUTING](./CONTRIBUTING.md)!

Please also see the above if you have a bug to report.
