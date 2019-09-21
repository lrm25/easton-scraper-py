import argparse
import getopt

from app import app

def parse(cmd_line_args):

    #gymOptions = ['all','arvada', 'aurora', 'boulder','castlerock','centennial','denver','littleton','thornton']

    parser = argparse.ArgumentParser()
    #parser.add_argument("-g", help="Easton gym", choices=gymOptions, default="all")
    #parser.add_argument("--gym", help="Easton gym", choices=gymOptions, default="all")
    args = parser.parse_args()
    boulder_schedule_id = app.get_boulder_schedule_id()
    print("Schedule ID:  %s" % (boulder_schedule_id))

    return 0

def printHelp():
    print("Usage: main.py -h|--help")