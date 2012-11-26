#!/usr/bin/env python
import datetime
import logging
import random
import sys
from os import fdopen

from board import Board

VERSION = 0.001


sys.stdout = fdopen(sys.stdout.fileno(), 'w', 0)

now = datetime.datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
logging.basicConfig(filename="log/cotigo.log",
                    format="%(asctime)s %(message)s",
                    level=logging.DEBUG)
log = logging
log.info("=== Starting ===")


class UnrecognizedCommand(Exception):
    pass


class ToDo(Exception):
    pass


class Cotigo(object):
    def __init__(self, size=19):
        self.canned_answers = {
            'name': "cotigo",
            'protocol_version': 2,
            'version': VERSION,
        }
        self.size = size
        self.clear()

    def clear(self):
        self.board = Board(self.size)

    def _cmd_list_commands(self, args):
        cmdlist = self.canned_answers.keys()
        for obj in dir(self):
            if obj.startswith("_cmd_"):
                cmdlist.append(obj[5:])
        return cmdlist

    def _cmd_boardsize(self, args):
        self.size = int(args[0])

    def _cmd_clear_board(self, args):
        self.clear()

    def _cmd_play(self, args):
        self.board.play(args[0], args[1][0], args[1][1:])

    def _cmd_genmove(self, args):
        while True:
            x = random.randint(0, 18)
            y = random.randint(0, 18)
            if self.board.squares[x][y] == ".":
                break
        self.board.play(args[0], x, y)
        return self.board.wacky(x) + str(y + 1)

    def process_command(self, raw_cmd):
        cmd = raw_cmd.strip()
        if cmd in self.canned_answers:
            return [self.canned_answers[cmd]]
        splitcmd = cmd.split(" ")
        if hasattr(self, "_cmd_" + splitcmd[0]):
            response = getattr(self, "_cmd_" + splitcmd[0])(splitcmd[1:])
            if response is None:
                response = [""]
            if not isinstance(response, list):
                response = [response]
            return response
        raise UnrecognizedCommand(raw_cmd)


def command_loop(cotigo):
    try:
        while True:
            cmd = sys.stdin.readline().strip()
            log.info("|||| %s", cmd)
            response = cotigo.process_command(cmd)
            for line in response:
                print "= %s" % line
                log.info("|||| = %s", response)
            print
    except KeyboardInterrupt:
        log.info("KeyboardInterrupt")
        raise

if __name__ == "__main__":
    cotigo = Cotigo()
    command_loop(cotigo)
