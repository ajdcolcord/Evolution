#!/usr/bin/env python2.7

import sys
import subprocess

TEST_PATH = "stream_tests/"
PYTHON2_PATH = "python2.7"


def xstream(testName, fileName):
    printing = testName + "\n\tresult: "
    try:
        result = subprocess.check_output([PYTHON2_PATH, sys.path[0] + "/xstream"], stdin=fileName)
        if not result:
            printing += "program quit\n"
        else:
            printing += result
    except Exception as e:
        printing += str(e)

    print printing


with open(TEST_PATH + "/reg-json-in.json", "r") as reg:
    xstream("regular json one-liner (count should be 1)", reg)

with open(TEST_PATH + "/split-in.json", "r") as split:
    xstream("one json expr split across lines (count should be 1)", split)

with open(TEST_PATH + "/two-split-in.json", "r") as two_split:
    xstream("two json exprs split and sharing lines (count should be 2)", two_split)

with open(TEST_PATH + "/plain-bools-in.json", "r") as bools:
    xstream("plain json booleans (count should be 2)", bools)
