"""Command line entry point: starts the loopback service (--data-dir, --port)."""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m algebra_notebook",
        description="Offline notebook for exact algebra in one real variable. "
        "The service listens on 127.0.0.1 only.",
    )
    parser.add_argument("--data-dir", default="./notebook-data",
                        help="directory for the SQLite notebook file (default: %(default)s)")
    parser.add_argument("--port", type=int, default=8765,
                        help="loopback port to listen on (default: %(default)s)")
    return parser


def main(argv=None) -> int:
    build_parser().parse_args(argv)
    print("not implemented yet: see #14 (loopback service)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
