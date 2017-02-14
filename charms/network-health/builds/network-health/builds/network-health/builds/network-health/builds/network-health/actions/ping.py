#!/usr/bin/python
import subprocess
import os
import sys
import json
from ast import literal_eval


from charmhelpers.core import (
    hookenv,
    host,
)

from charmhelpers.core.hookenv import (
    action_get,
    action_set,
)


def main():
    targets = hookenv.action_get('targets')
    hookenv.log("Got: {}".format(targets))
    # Undo the formatting passed into the action so juju didn't puke
    targets = targets.replace('=', ':')
    targets = targets.replace('(', '{')
    targets = targets.replace(')', '}')
    hookenv.log('Parsed to: {}'.format(targets))
    targets = json.loads(targets)
    results = {}
    # Get unit names from targets dict and ping their public address
    for target, ip in targets.items():
        results[target] = ping_check(ip)
    action_set({'results': results})


def ping_check(target):
    # If ping returns anything but success, return False
    try:
        output = subprocess.check_output("ping -c 1 " + target, shell=True)
    except Exception, e:
        return False

    return True


if __name__ == "__main__":
    main()
