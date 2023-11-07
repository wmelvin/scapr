#!/usr/bin/env python3

import argparse
import sys
import time

from collections import namedtuple
from datetime import datetime
from pathlib import Path
from PIL import ImageGrab

app_version = "231107.1"

pub_version = "0.1.dev2"

app_title = (
    "scapr - Screen Capture utility - version "
    f"{pub_version} (mod {app_version})"
)

AppOptions = namedtuple(
    "AppOptions", "out_path, sleep_seconds, stop_count, auto, region"
)

DEFAULT_SECONDS = 3

MAX_SECONDS = 60 * 60
#  Maximum interval between screenshots. An hour is already unlikely
#  to be useful.


def get_args(argv):
    ap = argparse.ArgumentParser(
        description="Command-line utility to capture screenshots."
    )

    ap.add_argument(
        "--auto",
        dest="auto",
        action="store_true",
        help="Do not prompt to start capturing screenshots. "
        "Begin right away.",
    )

    ap.add_argument(
        "--seconds",
        dest="sleep_sec",
        type=int,
        action="store",
        help="Number of seconds to pause between screenshots.",
    )

    ap.add_argument(
        "--count",
        dest="stop_count",
        type=int,
        action="store",
        help="Number of screenshots to take before stopping.",
    )

    ap.add_argument(
        "--folder",
        dest="output_dir",
        type=str,
        action="store",
        help="Name of folder for saving captured screenshots. ",
    )

    ap.add_argument(
        "--region",
        dest="region_box",
        type=str,
        action="store",
        help="Region to capture (instead of full screen). "
        "Specify box coordinates, separated by commas (no spaces between), "
        "as 'x1,y1,x2,y2' where x1 and y1 are the left-top pixel "
        "coordinates, and x2 and y2 are the right-bottom pixel "
        "coordinates. Example: '--region 100,100,600,600' to capture a "
        "500 x 500 image starting at 100 pixels from top and left.",
    )

    return ap.parse_args(argv[1:])


def get_opts(argv):
    args = get_args(argv)

    if args.output_dir is None:
        out_path = Path.cwd()
    else:
        out_path = Path(args.output_dir).expanduser().resolve()
        if not (out_path.exists() and out_path.is_dir()):
            sys.stderr.write(f"\nERROR: Folder not found: '{out_path}'\n")
            sys.exit(1)

    if args.sleep_sec is None:
        sleep_seconds = DEFAULT_SECONDS
    else:
        sleep_seconds = args.sleep_sec
        if sleep_seconds < 1 or MAX_SECONDS < sleep_seconds:
            sleep_seconds = DEFAULT_SECONDS

    region = None
    if args.region_box is not None:
        reg_err = ""
        a = args.region_box.split(",")
        if len(a) == 4:
            b = [int(s.strip()) for s in a]
            if (b[2] < b[0]) or (b[3] < b[1]):
                reg_err = (
                    "x2 and y2 must be greater than x1 and y1 respectively."
                )
            else:
                region = (b[0], b[1], b[2], b[3])
        else:
            reg_err = (
                "Expecting four integers separated by commas (no spaces)."
            )

        if 0 < len(reg_err):
            sys.stderr.write(
                f"\nERROR: Invalid region coordinates '{args.region_box}'.\n"
            )
            sys.stderr.write(f"{reg_err}\n")
            sys.exit(1)

    opts = AppOptions(
        out_path, sleep_seconds, args.stop_count, args.auto, region
    )

    return opts


def main(argv):
    print(f"\n{app_title}")

    opts = get_opts(argv)

    print('  Run "scap.py -h" (or --help) to see available options.\n')

    if opts.region is None:
        print("Capture full screen.")
    else:
        print(f"Capture screen region {opts.region}.")

    if opts.stop_count is None:
        counter = -1
    else:
        counter = opts.stop_count
        print(f"Number of screenshots to take is {counter}.")

    print(f"Number of seconds between screenshots is {opts.sleep_seconds}.")
    print(f"Screenshots will be saved to '{opts.out_path}'.")

    if not opts.auto:
        answer = input("\nContinue [Y,n]? ")
        if answer.lower() not in ["y", ""]:
            sys.exit(0)

    while counter != 0:
        if 0 < counter:
            remaining = f" ({counter} remaining)"
        else:
            remaining = ""

        print(
            f"\nCapturing screen{remaining}. Press [Ctrl]+[C] to stop.\n"
        )

        counter -= 1

        try:
            dt = datetime.now().strftime("%y%m%d_%H%M%S")
            save_path = opts.out_path / f"screenshot-{dt}.jpg"
            img = ImageGrab.grab(opts.region)
            img.save(save_path)
            time.sleep(opts.sleep_seconds)

        except KeyboardInterrupt:
            print("\n\nStopped.\n")
            return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
