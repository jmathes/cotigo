import logging
from pprint import pformat
logging.basicConfig(filename="log/cotigo.log",
                    format="%(asctime)s %(message)s",
                    level=logging.DEBUG)
log = logging


class Board(object):
    def __init__(self, size=19):
        self.squares = []
        for i in xrange(size):
            self.squares.append(["."] * size)

    def log_state(self):
        log.info(pformat(self.squares))
        for row in self.squares:
            log.info("".join(row))

    def unwacky(self, letter):
        if not isinstance(letter, basestring):
            return letter
        if letter[0] in '0123456789':
            return int(letter) - 1
        coord = ord(letter) - 65
        if coord > 8:
            return coord - 1
        return coord

    def wacky(self, coord):
        if coord > 8:
            coord += 1
        return chr(coord + 65)

    def play(self, color, x, y):
        x = self.unwacky(x)
        y = self.unwacky(y)
        log.info("x, y: %s, %s", x, y)
        self.squares[x][y] = color
        # self.log_state()
