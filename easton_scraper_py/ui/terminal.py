import argparse
import datetime
from datetime import date, datetime, timedelta
from pytz import timezone

from app import app
from data import easton_gym
from data.easton_gym import GYM_TUPLES, IDX_TAG_NAME

# Print data to either terminal or file
def print_line(line, output_filename):
    if output_filename == "":
        print(line)
        return
    with open(output_filename, "a") as output_file:
        output_file.write(line)
        output_file.write('\n')

#
# Print requested class info out to terminal which matches all parameters below
# and_strings, or_strings, not_strings:  see search functions above
# instructor:  string which can be used to search for classes by a certain teacher
# no_cancelled:  only print classes that are not cancelled
# ids:  print class IDs, which can be used to retrieve class description
#
def print_classes(class_start_date, number_of_days, and_strings, or_strings, not_strings,
                  instructor, no_cancelled, ids, output_file):

    if output_file != "" and os.path.exists(output_file):
        os.remove(output_file)
    matches = False
    for day_offset in range(number_of_days):
        day_match = False
        class_date_object = class_start_date + timedelta(days=day_offset)
        class_date = class_date_object.strftime("%Y-%m-%d")
        fancy_class_date = class_date_object.strftime("%A, %B %d, %Y")
        for gym_key in sorted(easton_gym.gym_dict.keys()):
            gym = easton_gym.gym_dict[gym_key]
            gym_match = False
            for easton_class in gym.get_classes(class_date):
                if app.string_searches(easton_class.get_name(), and_strings, or_strings, not_strings) and \
                   (instructor == "" or easton_class.get_instructor().lower().find(instructor) != -1) and \
                        not (easton_class.get_cancelled() and no_cancelled):
                    if not day_match:
                        print_line(" **** {} **** ".format(fancy_class_date), output_file)
                        day_match = True
                    if not gym_match:
                        print_line("", output_file)
                        print_line(" **** {} **** ".format(gym.get_name()), output_file)
                        print_line("", output_file)
                        gym_match = True
                        matches = True
                    print_line("{}, {}, {}, {}{}{}".format(easton_class.get_start_time(), easton_class.get_end_time(),
                          easton_class.get_name(), easton_class.get_instructor(),
                          ", {}".format(easton_class.get_id()) if ids else "",
                          ', CANCELLED' if easton_class.get_cancelled() else ""), output_file)
        if day_match:
            print_line("", output_file)
            print_line("", output_file)

    if not matches:
        print_line(" **** NO MATCHES **** ", output_file)
        print_line("", output_file)

    print_line(" ******************** ", output_file)
    print_line("", output_file)
    mountain_time = timezone('America/Denver')
    now = datetime.now(mountain_time)
    print_line("Data retrieved on {}".format(now.strftime("%b %d %Y %I:%M%P %Z")), output_file)


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
    day_group.add_argument("--date", help="Display classes on specific date (format:  YYYY-MM-DD)")
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
    parser.add_argument("-o", help="Output to file", default="")
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
        print_classes(class_date, args.days, args.and_string, args.or_string, args.not_string, args.teacher,
                      args.no_cancelled, args.ids, args.o)

    return 0

