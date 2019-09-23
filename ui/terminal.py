import argparse
import getopt
from datetime import date, datetime, timedelta

from app import app


def parse(cmd_line_args):

    # gymOptions = ['all','arvada', 'aurora', 'boulder','castlerock','centennial','denver','littleton','thornton']

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load", help="Only load classes from local disk", action='store_true')
    parser.add_argument("--tomorrow", help="Print tomorrow's classes", action='store_true')
    parser.add_argument("--weekday", help="Print classes for this upcoming weekday")
    parser.add_argument("--days", help="Total days to print", default=1, type=int)
    # parser.add_argument("-g", help="Easton gym", choices=gymOptions, default="all")
    # parser.add_argument("--gym", help="Easton gym", choices=gymOptions, default="all")
    args = parser.parse_args()

    if args.tomorrow:
        class_date = date.today() + timedelta(days=1)
    elif args.weekday:
        days_ahead = app.convert_weekday_to_days_ahead(args.weekday.lower())
        if days_ahead < 0:
            print("Invalid day name:  {}".format(args.weekday))
            return
        class_date = date.today() + timedelta(days=days_ahead)
    else:
        class_date = date.today()

    if args.load:
        app.print_boulder_classes(class_date, args.days)
    else:
        app.retrieve_boulder_classes(class_date, args.days)

    return 0

