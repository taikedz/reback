#!/usr/bin/env python3

""" Utility to read the output of `ip a` and print most pertinent details

Allows filtering on inet/inet6 scope values

Bonus: to find LAN IPv4 of the box, use `python3 read-ipa.py global noprefix -4`
"""

import os
import re
import pathlib
import argparse
from subprocess import Popen, PIPE

THIS = pathlib.Path(os.path.realpath(__file__))
HEREDIR = pathlib.Path(os.path.dirname(THIS))


class ParseError(Exception):
    pass


def cli_args():
    # further quick examples at https://dev.to/taikedz/ive-parked-my-side-projects-3o62
    parser = argparse.ArgumentParser()

    parser.add_argument("scopes", help="Scope filters - only display NICs with all specified scopes", nargs="*")
    parser.add_argument("--ip4", "-4", help="Do not print full output, print IPv4 address", action="store_true")
    parser.add_argument("--ip6", "-6", help="Do not print full output, print IPv6 address", action="store_true")
    parser.add_argument("--name", "-n", help="Do not print full output, print NIC name", action="store_true")
    parser.add_argument("--state", "-s", help="Do not print full output, print NIC state", action="store_true")
    parser.add_argument("--mac", "-m", help="Do not print full output, print NIC MAC address", action="store_true")

    args = parser.parse_args()
    args.defaults = not any([args.ip4, args.ip6, args.name, args.state, args.mac])

    return args

class NIC:
    def __init__(self, name, state):
        self.name = name
        self.state = state
        self.type = None
        self.mac = None

        self.ip4ip = None
        self.ip4scopes = None

        self.ip6ip = None
        self.ip6scopes = None

    def __str__(self):
        detail = [f"{self.name} ({self.type}, {self.state}) : {self.mac}"]
        if self.ip4ip:
            detail.append(f"  {self.ip4ip} -> {self.ip4scopes}")
        if self.ip6ip:
            detail.append(f"  {self.ip6ip} -> {self.ip6scopes}")

        return '\n'.join(detail)


def parse_ipa(data):
    lines = data.split("\n")
    # 1. break into blocks
    # 2. extract each block
    nics = []
    current_nic = None
    for L in lines:
        if m := re.match(r'\d+: ([a-z0-9@]+):.*?state ([A-Z]+)', L):
            if current_nic:
                nics.append(current_nic)
            current_nic = NIC(m.group(1), m.group(2) )

        elif current_nic is None:
            raise ParseError(f"Got a block inner line before a block was declared - line: {repr(L)}")

        elif m := re.match(r"link/([a-z0-9]+)\s+([a-f0-9:]+)", L.strip()):
            current_nic.type = m.group(1)
            current_nic.mac = m.group(2)

        elif m := re.match(r"inet\s+([0-9./]+).+?scope (.+)", L.strip()):
            current_nic.ip4ip = m.group(1)
            current_nic.ip4scopes = m.group(2)

        elif m := re.match(r"inet6\s+([0-9a-f:/]+).+?scope (.+)", L.strip()):
            current_nic.ip6ip = m.group(1)
            current_nic.ip6scopes = m.group(2)

    if current_nic:
        nics.append(current_nic)

    return nics


def main():
    args = cli_args()
    proc = Popen(["ip", "a"], stdout=PIPE)
    stdout, _ = proc.communicate()
    nics = parse_ipa(str(stdout, 'utf-8'))

    if args.scopes:
        nics = filter_scopes(nics, args.scopes)

    if args.defaults:
        [print(nic) for nic in nics]
    else:
        for nic in nics:
            details = []
            if args.name:
                details.append("NAME="+nic.name)
            if args.mac:
                details.append("MAC="+nic.mac)
            if args.state:
                details.append("STATE="+nic.mac)
            if args.ip4:
                if nic.ip4ip:
                    details.append(nic.ip4ip)
            if args.ip6:
                if nic.ip6ip:
                    details.append(nic.ip6ip)
            print(' '.join(details) )

def _or(val, check):
    return check if check else val

def filter_scopes(nics, scopes):
    remain = []
    for nic in nics:
        retain = True
        nic_scopes = _or('',nic.ip4scopes).split() + _or('',nic.ip6scopes).split()

        for scope in scopes:
            if scope not in nic_scopes:
                retain = False
                break
        if retain:
            remain.append(nic)
    return remain

# Generic launch and catch assertions
if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        # Catches all exceptions, but not KeyboardInterrupt

        # Normally silence tracebacks. Run with PY_TRACEBACK=true to show them
        if os.getenv("PY_TRACEBACK") == "true":
            raise
        else:
            print(e)
            exit(1)
