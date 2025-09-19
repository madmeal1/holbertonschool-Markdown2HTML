#!/usr/bin/python3
"""Converts a Markdown file to HTML file."""
import sys
import os
import re
import hashlib


def apply_formatting(text):
    """Replace Markdown bold/emphasis by HTML tags\
          and apply special formatting."""
    text = apply_special_formatting(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<em>\1</em>", text)
    return text


def apply_special_formatting(text):
    """Apply [[MD5]] and ((remove C)) transformations."""
    def md5_replace(match):
        value = match.group(1)
        md5 = hashlib.md5(value.encode()).hexdigest()
        return md5

    text = re.sub(r"\[\[(.+?)\]\]", md5_replace, text)

    def remove_c(match):
        value = match.group(1)
        return re.sub(r"[cC]", "", value)

    text = re.sub(r"\(\((.+?)\)\)", remove_c, text)

    return text


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
                content = apply_formatting(match.group(2))
                html.write("<h{}>{}</h{}>\n".format(level, content, level))
                continue

            if line.startswith("- "):
                if in_p:
                    html.write("</p>\n")
                    in_p = False
                if not in_ul:
                    html.write("<ul>\n")
                    in_ul = True
                html.write(
                    "<li>{}</li>\n".format(apply_formatting(line[2:].strip()))
                )
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
                html.write(
                    "<li>{}</li>\n".format(apply_formatting(line[2:].strip()))
                )
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
                    html.write(apply_formatting(line) + "\n")
                else:
                    html.write("<br/>\n" + apply_formatting(line) + "\n")

        if in_ul:
            html.write("</ul>\n")
        if in_ol:
            html.write("</ol>\n")
        if in_p:
            html.write("</p>\n")

    sys.exit(0)
