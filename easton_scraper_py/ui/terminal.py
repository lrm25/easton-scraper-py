import argparse
from datetime import date, datetime, timedelta

from app import app
from data.easton_gym import GYM_TUPLES, IDX_TAG_NAME


#
# get command line arguments and send to application code to be processed
#
def parse():

    gym_options = [gym_tuple[IDX_TAG_NAME] for gym_tuple in GYM_TUPLES]
    max_days_allowed = 10

    print()
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument("--load", help="Only load classes from local disk", action='store_true')
    day_group = parser.add_mutually_exclusive_group()
    day_group.add_argument("--tomorrow", help="Print tomorrow's classes", action='store_true')
    day_group.add_argument("--weekday", help="Print classes for this upcoming weekday")
    day_group.add_argument("--date", help="Display classes on specific date (format:  YYYY-MM-DD")
    parser.add_argument("--days", help="Total days to print", default=1, type=int)
    parser.add_argument("--delete", help="Delete old classes", action='store_true')
    parser.add_argument("--gym", help="Search these gyms' schedules only", choices=gym_options, default=[],
                        action='append', dest='gyms')
    parser.add_argument("--and", help="AND search by string", default=[], action='append', dest='and_string')
    parser.add_argument("--or", help="OR search by string", default=[], action='append', dest='or_string')
    parser.add_argument("--not", help="NOT search by string", default=[], action='append', dest='not_string')
    parser.add_argument("--teacher", help="Search for classes by instructor", default="")
    parser.add_argument("--no-cancelled", help="Don't display cancelled classes", default=False, action='store_true')
    parser.add_argument("--ids", help="Display class IDs to get description", action='store_true')
    parser.add_argument("--description", help="Get description for class with this ID", default="")
    args = parser.parse_args()

    # If user specifies, delete classes yesterday and before
    if args.delete:
        app.delete_old_classes()

    # check day parameter
    if max_days_allowed < args.days:
        print("Number of days: {} is too large, max allowed is {}".format(args.days, max_days_allowed))
        return
    if args.days < 1:
        print("Invalid number of days:  {}".format(args.days))
        return

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

    # Since different gyms could possibly have same ID for class (I don't actually know), play it safe
    if args.description != "":
        if not args.gyms or 1 < len(args.gyms):
            raise TypeError("Must have exactly one gym value when retrieving description")

    # Either load classes from "db" or retrieve from internet
    if args.load:
        if not app.load_classes(class_date, args.gyms, args.days):
            return 0
    else:
        app.retrieve_classes(class_date, args.gyms, args.days)
        print()
        print()

    if args.description != "":
        try:
            description = app.get_class_description(args.gyms[0], args.description)
            print(description)
        except ValueError as e:
            print(e)
    else:
        app.print_classes(class_date, args.days, args.and_string, args.or_string, args.not_string, args.teacher,
                          args.no_cancelled, args.ids)

    return 0

