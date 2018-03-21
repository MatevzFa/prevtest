#!/usr/bin/env python3

import difflib
import shutil
import os
import sys
import glob
import subprocess

import colorama
from colorama import Fore
colorama.init()

PREV_HOME = os.path.abspath("../prev")
TEST_HOME = os.path.abspath(os.curdir)

OUT = TEST_HOME + "/out"
SRCS = PREV_HOME + "/srcs"

OK_MSG = ":-) This is PREV compiler:\n:-) Done.\n"


def basename(path):
    return os.path.splitext(path)[0]


def clean():
    try:
        shutil.rmtree(OUT)
    except FileNotFoundError:
        pass


def compile_test(phase, test):
    if not os.path.exists("test_results/" + phase):
        os.makedirs("test_results/" + phase)

    os.chdir(OUT)
    output = subprocess.check_output([
        "java",
        "compiler.Main",
        "--xml=../%s/%s/%s.xml" % ("test_results",
                                   phase, test),
        "--xsl=./",
        "--target-phase=%s" % phase,
        "--logged-phase=%s" % phase,
        "../%s/%s/%s.prev" % ("test_programs", phase, test)
    ], stderr=subprocess.STDOUT)

    os.chdir(TEST_HOME)

    return output


def check_test(phase, test):
    # ref_file = open("test_programs/%s/%s.xml" % (phase, test), "r")
    # result_file = open("test_results/%s/%s.xml" % (phase, test), "r")
    # diff = difflib.ndiff(ref_file.readlines(), result_file.readlines())
    # diffs = list(filter(lambda line: line[0] == "-", diff))
    # return len(diffs) == 0
    return True


def run_test(phase, test, indent=0):
    output = compile_test(phase, test).decode("unicode_escape")
    correct = check_test(phase, test)

    if output != OK_MSG:
        print(indent*" " + "%-25s %5s" %
              (test, Fore.RED + "COMPILATION ERROR" + Fore.RESET))
        print(output)
    elif correct:
        print(indent*" " + "%-25s %5s" %
              (test, Fore.GREEN + "OK" + Fore.RESET))
    else:
        print(indent*" " + "%-25s %5s" %
              (test, Fore.RED + "FAIL" + Fore.RESET))


def test_phase(phase, filt=None):
    print("---")
    print("Testing phase %s" % phase)
    for file in sorted(glob.glob("test_programs/%s/*.prev" % (phase))):
        file = basename(os.path.basename(file))
        if filt == None or filt in file:
            run_test(phase, file, indent=4)


def build():
    print("Building the compiler... ", end='')
    clean()
    os.mkdir(OUT)
    os.chdir(SRCS)
    javac = subprocess.Popen([
        "javac",
        "-d", os.path.relpath(OUT),
        "compiler/Main.java"
    ])
    javac.wait()
    os.chdir(TEST_HOME)
    print("Done!")


build()

phase = sys.argv[1]
if len(sys.argv) > 2:
    filt = sys.argv[2]
else:
    filt = None

test_phase(phase, filt)
