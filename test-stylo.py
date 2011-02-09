#!/usr/bin/python

import os

from subprocess import *

if __name__ == "__main__":
    test_module_names = os.listdir("./tests/")

for tmn in test_module_names:
    if tmn.endswith(".py"):
        Popen(["python", "tests/%s" % tmn]).communicate()
