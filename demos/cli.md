# `pymor` CLI

This demo shows how the `pymor` cli works. Below are copy/paste examples, with
example output (version 0.2.1):

### Running the command without anything
```
$ pymor

 Usage: pymor [OPTIONS] COMMAND [ARGS]...

 PyMOR - Makes CMOR Simple

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                     Show the version and exit.                                                                    │
│ --verbose               -v    Log debugging info to stderr.                                                                 │
│ --quiet                 -q    Suppress info to stderr.                                                                      │
│ --logfile/--no-logfile        Log to file. [default: logfile]                                                               │
│ --profile_mem                 Profile peak memory use.                                                                      │
│ --help                        Show this message and exit.                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ cache                                                                                                                       │
│ develop                                                                                                                     │
│ externals           Information about external dependencies                                                                 │
│ plugins             Manage pymor plugins                                                                                    │
│ prefect-check                                                                                                               │
│ process                                                                                                                     │
│ scripts             Various utility scripts for Pymor.                                                                      │
│ ssh-tunnel          Create an SSH tunnel to access Prefect and Dask dashboards on a remote compute node.                    │
│ table-explorer                                                                                                              │
│ validate                                                                                                                    │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### Checking the version
```
$ pymor --version
pymor, version 0.2.1
```

### Getting help for various subcommands
```
$ pymor process --help

 Usage: pymor process [OPTIONS] CONFIG_FILE

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


$ pymor cache --help

 Usage: pymor cache [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                     Show the version and exit.                                                                    │
│ --verbose               -v    Log debugging info to stderr.                                                                 │
│ --quiet                 -q    Suppress info to stderr.                                                                      │
│ --logfile/--no-logfile        Log to file. [default: logfile]                                                               │
│ --profile_mem                 Profile peak memory use.                                                                      │
│ --help                        Show this message and exit.                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ inspect-prefect-global               Print information about items in Prefect's storage cache                               │
│ inspect-prefect-result                                                                                                      │
│ populate-cache                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


$ pymor validate --help

 Usage: pymor validate [OPTIONS] COMMAND [ARGS]...

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version                     Show the version and exit.                                                                    │
│ --verbose               -v    Log debugging info to stderr.                                                                 │
│ --quiet                 -q    Suppress info to stderr.                                                                      │
│ --logfile/--no-logfile        Log to file. [default: logfile]                                                               │
│ --profile_mem                 Profile peak memory use.                                                                      │
│ --help                        Show this message and exit.                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ config                                                                                                                      │
│ directory                                                                                                                   │
│ table                                                                                                                       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
## Dealing with the Prefect Cache

In some circumstances, you may want to inspect the Prefect cache. You can use `pymor cache` to help with 
that. If you want to purge the cache, you can just remove the files, normally under `~/.prefect/storage/`.
