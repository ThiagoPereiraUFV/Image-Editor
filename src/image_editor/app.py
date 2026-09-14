"""Composition root: wires the real terminal streams and Pillow's show() into Menu."""

import sys

from image_editor import image_io
from image_editor.menu import Menu


def main():
    try:
        Menu(sys.stdin, sys.stdout, image_io.show).run()
    except EOFError, KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
