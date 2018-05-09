#!/usr/bin/env python3

from xmlcompare import XmlTree

import difflib
import shutil
import os
import sys
import glob
import subprocess
import re
import argparse
import time

import colorama
from colorama import Fore
colorama.init()

"""
Constants
"""
PREV_HOME = os.path.abspath("../prev")
TEST_HOME = os.path.abspath(os.curdir)
BUILD_DIR = TEST_HOME + "/out"
SRCS = PREV_HOME + "/srcs"
OK_MSG = ":-) This is PREV compiler:" + os.linesep + ":-) Done." + os.linesep
OK_MSG_INTERPRETER = ":-) This is PREV compiler:" + os.linesep + "1" + os.linesep + ":-) Done." + os.linesep

xmltree = XmlTree()


def basename(path):
    return os.path.splitext(path)[0]


def clean():
    try:
        shutil.rmtree(BUILD_DIR)
    except FileNotFoundError:
        pass


def compile_test(phase, test):
    os.makedirs("test_results/" + phase, exist_ok=True)

    if not os.path.isfile("test_results/%s/%s.xsl" % (phase, phase)):
        shutil.copy(
            "%s/data/%s.xsl" % (PREV_HOME, phase),
            "test_results/%s/%s.xsl" % (phase, phase)
        )

    os.chdir(BUILD_DIR)

    if args.verbose:
        print("Compiling test %s... " % test, end='')

    output = subprocess.check_output([
        "java",
        "compiler.Main",
        "--xml=../%s/%s/%s.xml" % ("test_results", phase, test),
        "--xsl=./",
        "--target-phase=%s" % phase,
        "--logged-phase=%s" % phase,
        "../%s/%s/%s.prev" % ("test_programs", phase, test)
    ], stderr=subprocess.STDOUT)

    if args.verbose:
        print("Done!")
        print(output)

    os.chdir(TEST_HOME)

    return output


def check_test(phase, test):
    expected_xml_file = "test_programs/%s/%s.xml" % (phase, test)
    xml_file = "test_results/%s/%s.xml" % (phase, test)
    return xmltree.xml_files_compare(expected_xml_file, xml_file, excludes=["location", "loc"])


def test_should_fail(test):
    return "fail" in test.lower()


def print_test_result(test, color, message, indent=0, note=""):
    print(indent*" " + "%-25s %5s %s" % (test, color + message + Fore.RESET, note))


def run_test(phase, test, indent=0):
    output = compile_test(phase, test).decode("unicode_escape")
    compile_ok = output == OK_MSG or output == OK_MSG_INTERPRETER
    fail_test = test_should_fail(test)

    if compile_ok and fail_test:
        print_test_result(test, Fore.RED, "ERROR UNDETECTED", indent)
        return
    if not compile_ok and not fail_test:
        print_test_result(test, Fore.RED, "COMPILATION ERROR", indent)
        if args.verbose:
            print(output)
        return

    # Check that XML is correct only in case it has actually compiled
    if compile_ok:
        correct_xml = check_test(phase, test)
        if not correct_xml:
            print_test_result(test, Fore.RED, "WRONG XML", indent)
            return

    # Every check passed
    err_text = output.split(":-( ")[-1].replace(os.linesep, " ") if fail_test else ""
    note = err_text if args.verbose else ""
    print_test_result(test, Fore.GREEN, "OK", indent, note=note)


def natural_sort(arr):

    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    arr.sort(key=alphanum_key)
    return arr


def test_phase(phase, filt=None):
    print("---")
    print("Testing phase %s" % phase)
    for file in natural_sort(glob.glob("test_programs/%s/*.prev" % (phase))):
        test = basename(os.path.basename(file))
        if filt is None or filt in test:
            run_test(phase, test, indent=4)


def build():
    print("Building the compiler... ", end='')
    sys.stdout.flush()
    clean()
    os.mkdir(BUILD_DIR)
    os.chdir(SRCS)
    javac = subprocess.Popen([
        "javac",
        "-d", os.path.relpath(BUILD_DIR),
        "compiler/Main.java"
    ])
    javac.wait()
    os.chdir(TEST_HOME)
    print("Done!")


def update_tests(phase):
    print("Updating tests for phase %s... " % (phase), end='')
    sys.stdout.flush()

    os.makedirs("test_programs/" + phase, exist_ok=True)

    for test_program in glob.glob("%s/test_programs/%s/*.prev" % (TEST_HOME, phase)):
        test = basename(os.path.basename(test_program))
        if "fail" in test:
            continue

        compile_test(phase, test)
        shutil.copy("test_results/%s/%s.xml" % (phase, test), "test_programs/" + phase)

        # clean tmp test_results
        shutil.rmtree("test_results/" + phase)
        if not os.listdir("test_results"):
            os.rmdir("test_results")

    print("Done!")


"""
Command line interface
"""
parser = argparse.ArgumentParser()

parser.add_argument("phase", metavar="PHASE", type=str, help="Target phase")
parser.add_argument("filter", metavar="FILTER", type=str, nargs="?", help="Filter for test cases")

parser.add_argument("--update-tests",  dest="updatetests", action="store_true", help="Update tests for some phase")
parser.add_argument("--verbose",  dest="verbose", action="store_true", help="Verbose output")
parser.add_argument("--no-build", dest="build", action="store_false", help="Don't rebuild the compiler")

args = parser.parse_args()

"""
Start
"""
if args.build:
    build()

if args.updatetests:
    update_tests(args.phase)


test_phase(args.phase, args.filter)
