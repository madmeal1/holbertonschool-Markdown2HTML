#!/usr/bin/python3
"""Converts a Markdown file to HTML file."""
import sys
import os

"""Converts a Markdown file to HTML file."""
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print("Missing {}".format(input_file), file=sys.stderr)
        sys.exit(1)

        pass

    sys.exit(0)
