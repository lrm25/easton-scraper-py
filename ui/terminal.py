import argparse
import getopt

from app import app

def parse(cmdLineArgs):

    gymOptions = ['all','arvada', 'aurora', 'boulder','castlerock','centennial','denver','littleton','thornton']

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-g", help="Easton gym", choices=gymOptions, default="all")
        parser.add_argument("--gym", help="Easton gym", choices=gymOptions, default="all")
        args = parser.parse_args()
        print(args)
        #app.getData()

    except getopt.error as err:
        print(str(err))
        printHelp()
        return -1
    return 0

def printHelp():
    print("Usage: main.py -h|--help")