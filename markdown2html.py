#!/usr/bin/python3
"""Converts a Markdown file to HTML file."""
import sys
import os
import re


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print("Missing {}".format(input_file), file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r") as md, open(output_file, "w") as html:
        for line in md:
            line = line.rstrip("\n")
            match = re.match(r"^(#{1,6}) (.*)", line)
            if match:
                level = len(match.group(1))
                content = match.group(2)
                html.write("<h{}>{}</h{}>\n".format(level, content, level))

    sys.exit(0)
