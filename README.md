# pyretry

A simple script for retrying simple commands if they fail.

To use:

    usage: retry [-h] [--tries TRIES] [--time TIME] [--output OUTPUT] [--verbose] -- [COMMAND ...]

    positional arguments:
    COMMAND          The command to run

    options:
    -h, --help       show this help message and exit
    --tries TRIES    Maximum number of tries to attempt (default: 3)
    --time TIME      Maximum time to keep attempting in seconds (default: 12 hours)
    --output OUTPUT  File to redirect output to (default: don't change)
    --verbose        More verbose output

The options available are straightforward:

* **tries** - run the command up to this many times before giving up. If the command still fails after the `tries`'th time, exit with its last return code.
* **time** - keep trying for this many seconds before giving up. If we've been trying for longer than this, exit with its last return code. This is only checked before executing a command, so if you set a limit of 300 seconds and an attempt ends at 299 seconds, it will run another attempt. It will never cancel an attempt that is already running.
* **output** - a filename to redirect both stdout and stderr to. The file will be overwritten if it exists. This file will only be opened once, and all subsequent output from all attempts will be written to it (with a header line before each attempt)
* **verbose** - more verbose output from time to time