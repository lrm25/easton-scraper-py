import argparse
import getopt
from datetime import date, datetime, timedelta

from app import app


def parse(cmd_line_args):

    gym_options = ['all', 'arvada', 'aurora', 'boulder', 'castlerock', 'centennial', 'denver', 'littleton', 'thornton']

    parser = argparse.ArgumentParser()
    parser.add_argument("--load", help="Only load classes from local disk", action='store_true')
    parser.add_argument("--tomorrow", help="Print tomorrow's classes", action='store_true')
    parser.add_argument("--weekday", help="Print classes for this upcoming weekday")
    parser.add_argument("--days", help="Total days to print", default=1, type=int)
    parser.add_argument("--delete", help="Delete old classes", action='store_true')
    parser.add_argument("--gym", help="Easton gym", choices=gym_options, default=[], action='append', dest='gyms')
    parser.add_argument("--and", help="AND search by string", default=[], action='append', dest='and_string')
    parser.add_argument("--or", help="OR search by string", default=[], action='append', dest='or_string')
    parser.add_argument("--not", help="NOT search by string", default=[], action='append', dest='not_string')
    parser.add_argument("--teacher", help="Search for classes by instructor", default="")
    parser.add_argument("--date", help="Display classes on specific date (format:  YYYY-MM-DD")
    parser.add_argument("--no-cancelled", help="Don't display cancelled classes", default=False, action='store_true')
    parser.add_argument("--ids", help="Display class IDs to get description", action='store_true')
    parser.add_argument("--description", help="Get description for class with this ID", default="")
    args = parser.parse_args()

    if args.delete:
        app.delete_old_classes()
    if args.tomorrow:
        class_date = date.today() + timedelta(days=1)
    elif args.weekday:
        days_ahead = app.convert_weekday_to_days_ahead(args.weekday.lower())
        if days_ahead < 0:
            print("Invalid day name:  {}".format(args.weekday))
            return
        class_date = date.today() + timedelta(days=days_ahead)
    elif args.date:
        class_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        class_date = date.today()

    print(args.gyms)
    if args.load:
        app.load_boulder_classes(class_date, args.gyms, args.days)
    else:
        app.retrieve_boulder_classes(class_date, args.gyms, args.days)
    if args.description != "":
        # TODO change!  specify only one gym field
        app.get_class_description(args.gyms[0], args.description)
    else:
        app.print_boulder_classes(class_date, args.days, args.and_string, args.or_string, args.not_string, args.teacher,
                              args.no_cancelled, args.ids)

    return 0

