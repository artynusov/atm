from __future__ import print_function
import sys
from abc import ABCMeta, abstractproperty, abstractmethod

from atm import Atm


def error(msg):
    print('Error: {}'.format(msg), file=sys.stderr)


class CommandError(Exception):
    pass


class BaseCommand(object):
    __metaclass__ = ABCMeta

    name = abstractproperty()
    argc = abstractproperty()
    help = abstractproperty()

    @abstractmethod
    def _handle(self, args):
        pass

    def handle(self, args):
        if len(args) != self.argc:
            raise CommandError("Invalid arguments count")
        self._handle(args)


class InitCommand(BaseCommand):
    argc = 1
    name = "init"
    help = "Init ATM with notes in comma-separated format (e.g. 50=1,20=3)"

    def _handle(self, args):
        notes = {}
        try:
            for a in args[0].split(","):
                note, count = a.split("=")
                notes[int(note)] = int(count)
        except ValueError:
            raise CommandError("Incorrect format, should be comma-separated "
                               "<note>=<count>")
        a = Atm()
        a.notes.init(notes)


class StatusCommand(BaseCommand):
    argc = 0
    name = "status"
    help = "Show note counts"

    def _handle(self, args):
        result = []
        atm = Atm()
        for i in sorted(atm.notes.get_notes().items(), reverse=True):
            result.append("${}: {}".format(*i))
        print("\n".join(result))


class DispenseCommand(BaseCommand):
    argc = 1
    name = "dispense"
    help = "Dispense cash from ATM"

    def _handle(self, args):
        atm = Atm()
        result = atm.dispense(int(args[0]))
        if result:
            print("Dispensed successfully in following notes: {}".format(
                ", ".join(["${}".format(r) for r in result])))
        else:
            print("Unable to dispense requested amount")


COMMANDS = [InitCommand(), StatusCommand(), DispenseCommand()]


def print_help():
    print("ATM simulator, available commands:\n")
    for c in COMMANDS:
        print("{} -- {}".format(c.name, c.help))


def main(args):
    cmd_dict = dict((c.name, c) for c in COMMANDS)

    if len(args) == 1:
        print_help()
    elif args[1] not in cmd_dict:
        error('Unknown command')
    else:
        cmd = cmd_dict[args[1]]
        try:
            cmd.handle(args[2:])
        except CommandError, e:
            error(e)

if __name__ == '__main__':
    main(sys.argv)
