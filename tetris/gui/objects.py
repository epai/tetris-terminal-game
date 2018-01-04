import textwrap
from contextlib import contextmanager

from tetris.core import Pos

def clean_and_split(string):
    lines = textwrap.dedent(string.strip()).splitlines()
    return [l.strip() for l in lines if l.strip()]

class Box:
    def __init__(self, *args, min_height=3, min_width=34):
        self.min_height = min_height
        self.min_width = min_width
        self.lines = []

        for i, text in enumerate(args):
            bottom = 0 if i == len(args) - 1 else 1
            self.add_text(text, bottom=bottom)

    def add_text(self, text, top=0, bottom=0, color=None):
        pad = (('', color),)
        if not text:
            self.lines.extend(pad)
        else:
            lines = clean_and_split(text)
            self.lines.extend(pad * top)
            self.lines.extend(zip(lines, (color,) * len(lines)))
            self.lines.extend(pad * bottom)
            longest_line = max(len(line) for line in lines)
            self.min_width = max(self.min_width, longest_line)
            return self # for fluid interface

    def render(self, ui, pos=None):
        actual_height = len(self.lines)
        pad_amount = max(0, self.min_height - actual_height)
        pos = pos or Pos(
            ui.height // 2 - max(self.min_height, actual_height) // 2,
            ui.width // 2 - self.min_width // 2 - 1)

        offset = 0
        def add_line(line, color=None):
            nonlocal offset
            color = color or ui.board_color
            ui.stdscr.addstr(pos.y + offset, pos.x, line, color)
            offset += 1
        def add_lines(lines, colored=False):
            for line in lines:
                color = None
                if colored:
                    line, color = line
                add_line(line, color)

        center = '-'*self.min_width
        pad = '|{}|'.format(' '*self.min_width)
        lines = (('|{}|'.format(l.center(self.min_width)), c) for l,c in self.lines)

        add_line('┌{}┐'.format(center))
        add_lines((pad,) * (pad_amount // 2))
        add_lines(lines, colored=True)
        add_lines((pad,) * (pad_amount // 2 + pad_amount % 2))
        add_line('└{}┘'.format(center))


class Dialog(Box):
    def __init__(self, *args, min_height=3, min_width=34, **kwargs):
        super().__init__(*args, min_height=min_height, min_width=min_width)
        self.add_keys(**kwargs)

    def add_keys(self, **kwargs):
        self.keys = kwargs.keys()
        self.add_text(None) # ne
        for key, msg in kwargs.items():
            self.add_text("Press `{}` to {}".format(key, msg))
        return self

    @contextmanager
    def response(self, ui):
        self.render(ui)
        with ui.get_key(self.keys, delay=True) as key:
            yield key