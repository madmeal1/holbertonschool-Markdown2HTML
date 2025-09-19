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
        in_ul = False
        in_ol = False
        in_p = False

        for line in md:
            line = line.rstrip()

            match = re.match(r"^(#{1,6}) (.*)", line)
            if match:
                if in_p:
                    html.write("</p>\n")
                    in_p = False
                level = len(match.group(1))
                content = match.group(2)
                html.write("<h{}>{}</h{}>\n".format(level, content, level))
                continue

            if line.startswith("- "):
                if in_p:
                    html.write("</p>\n")
                    in_p = False
                if not in_ul:
                    html.write("<ul>\n")
                    in_ul = True
                html.write("<li>{}</li>\n".format(line[2:].strip()))
                continue
            else:
                if in_ul:
                    html.write("</ul>\n")
                    in_ul = False

            if line.startswith("* "):
                if in_p:
                    html.write("</p>\n")
                    in_p = False
                if not in_ol:
                    html.write("<ol>\n")
                    in_ol = True
                html.write("<li>{}</li>\n".format(line[2:].strip()))
                continue
            else:
                if in_ol:
                    html.write("</ol>\n")
                    in_ol = False

            if line.strip() == "":
                if in_p:
                    html.write("</p>\n")
                    in_p = False
                continue
            else:
                if not in_p:
                    html.write("<p>\n")
                    in_p = True
                    html.write(line + "\n")
                else:
                    html.write("<br/>\n" + line + "\n")

        if in_ul:
            html.write("</ul>\n")
        if in_ol:
            html.write("</ol>\n")
        if in_p:
            html.write("</p>\n")

    sys.exit(0)
