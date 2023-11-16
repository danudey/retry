#!/usr/bin/env python3

import sys
import time
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tries", type=int, default=3, help="Maximum number of tries to attempt (default: 3)")
    parser.add_argument("--time", type=int, default=43200, help="Maximum time to keep attempting in seconds (default: 12 hours)")
    parser.add_argument("--output", type=str, help="File to redirect output to (default: don't change)")
    parser.add_argument("--verbose", action="store_true", help="More verbose output")
    parser.add_argument("COMMAND", nargs="+")

    args = parser.parse_args()

    attempts = 0
    returncode = None
    start_time = time.monotonic()
    max_end_time = start_time + args.time

    command_kwargs = {}
    output_file = None

    if args.verbose:
        if args.output:
            output_text = f"outputting stdout/stderr to {args.output}"
        else:
            output_text = "not intercepting stdout/stderr"
        print(f"Running with {args.tries} attempts, to a maximum of {args.time} seconds, {output_text}", file=sys.stderr)

    if args.output:
        output_file = open(args.output, "wb")
        command_kwargs["stdout"] = output_file
        command_kwargs["stderr"] = output_file

    while attempts < args.tries and time.monotonic() < max_end_time:
        attempts += 1
        if args.verbose:
            print(f"[INFO][Attempt {attempts}] {' '.join(args.COMMAND)} ", file=sys.stderr)
        if output_file:
            output_file.write(f"===== Executing command attempt {attempts}: {' '.join(args.COMMAND)}\n".encode())
            output_file.flush()
        cmd = subprocess.Popen(args.COMMAND, **command_kwargs)
        returncode = cmd.wait()
        print(f"[INFO][Attempt {attempts}] exited with code {returncode} ", file=sys.stderr)
        if returncode == 0:
            break

    if returncode != 0:
        if attempts >= args.tries:
            print(f"[ERROR] Max retries reached, aborting")
        elif time.monotonic() >= max_end_time:
            print(f"[ERROR] Max time reached, aborting")
        else:
            print(f"[ERROR] Exited but we don't know why, aborting")
        sys.exit(returncode)

if __name__ == '__main__':
    main()