import argparse
import getopt

from app import app

def parse(cmd_line_args):

    #gymOptions = ['all','arvada', 'aurora', 'boulder','castlerock','centennial','denver','littleton','thornton']

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load", help="Only load classes from local disk", action='store_true')
    #parser.add_argument("-g", help="Easton gym", choices=gymOptions, default="all")
    #parser.add_argument("--gym", help="Easton gym", choices=gymOptions, default="all")
    args = parser.parse_args()
    if args.load:
        app.print_boulder_classes()
    else:
        app.retrieve_boulder_classes()

    return 0

def printHelp():
    print("Usage: main.py -h|--help")