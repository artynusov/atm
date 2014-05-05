# ATM emulator

## Usage

ATM emulator provides simple command line interface.

Initialize ATM with money:

    python cli.py <comma-separated list with note counts, e.g. 50=5,20=10>

Show current note counts:

    python cli.py status

Dispense money from ATM

    python cli.py dispense <amount>

## Requirements

* Python 2.7
* [mock](http://www.voidspace.org.uk/python/mock/mock.html) library for unit testing