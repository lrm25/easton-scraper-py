import calendar
import datetime
from datetime import date, timedelta
import os

from data import easton_gym
from data.easton_gym import EastonGym
import storage.db as db

from . import easton_calendar, mindbody_calendar, zen_calendar


#
# Convert weekday option to numerical day parameter, so this parameter can be added to the current day to get the
# desired date.
#
def convert_weekday_to_days_ahead(weekday):

    day_list = [day_name.lower() for day_name in list(calendar.day_name)]
    try:
        day_index = day_list.index(weekday)
    except ValueError:
        return -1

    day_index += 7
    return day_index - date.today().weekday()


#
# Delete easton classes stored in local files, that have completed before the time the user queries this function.
#
def delete_old_classes():

    db.delete_classes_done_before_now()


#
# Retrieve all class data from the internet, for the given gyms (all if 'gyms' is empty), the starting class date,
# and for the total number of days starting with that starting class date
#
def retrieve_classes(class_date, gyms, number_of_days):
    
    easton_calendar.get_and_parse_gyms_data(gyms, class_date, number_of_days)


#
# Load classes from disk or db
# Return:  True if any classes loaded, False if not
#
def load_classes(class_start_date, gyms, number_of_days):

    class_day_list = []
    for day_offset in range(number_of_days):
        offset_date = class_start_date + timedelta(day_offset)
        class_day_list.append(offset_date.strftime("%Y-%m-%d"))
    easton_classes = db.load(class_day_list)
    if not len(easton_classes):
        print(" *** No classes found.  Try removing --load tag to retrieve *** ")
        return False

    for easton_class in easton_classes:
        gym_db_name = easton_class.get_gym_db_name()
        if not len(gyms) or gym_db_name in gyms:
            try:
                gym = easton_gym.gym_dict[gym_db_name]
            except KeyError:
                if not easton_gym.gym_tuple_idx_map:
                    easton_gym.create_tuple_map()
                gym = EastonGym(easton_gym.gym_tuple_idx_map[gym_db_name])
                easton_gym.gym_dict[gym_db_name] = gym
            gym.add_class(easton_class)
    for gym in easton_gym.gym_dict.values():
        gym.sort_classes()
    return True


#
# Return true if the class name contains one of the OR strings
#
def or_search(easton_class_name, or_strings):

    if not or_strings:
        return True
    for or_string in or_strings:
        if easton_class_name.find(or_string) != -1:
            return True
    return False


#
# Return true if the class name does not contain any of the NOT strings
#
def not_search(easton_class_name, not_strings):
    if not not_strings:
        return True
    for not_string in not_strings:
        if easton_class_name.find(not_string) != -1:
            return False
    return True


#
# Return true if the class name contains all of the AND strings
#
def and_search(easton_class_name, and_strings):

    if not and_strings:
        return True
    for and_string in and_strings:
        if easton_class_name.find(and_string) == -1:
            return False
    return True


#
# AND, OR, and NOT search the easton class name depending on what the user wants (see each individual
# function for descriptions)
#
def string_searches(easton_class_name, and_strings, or_strings, not_strings):

    lowercase_name = easton_class_name.lower()
    return and_search(lowercase_name, and_strings) and or_search(lowercase_name, or_strings) and \
        not_search(lowercase_name, not_strings)


#
# get class description from webpage, using gym name and class ID
#
def get_class_description(gym_name, class_id):

    if gym_name == 'castlerock':
        gym_name = 'Castle_Rock'

    link = db.get_class_description_link(gym_name, class_id)
    if gym_name == 'Castle_Rock' or gym_name == 'Thornton':
        description = zen_calendar.get_class_description(link)
    else:
        description = mindbody_calendar.get_class_description(link)

    return description

# TODO print code should be in UI
# Print data to either terminal or file
def print_line(line, output_filename):
    if output_filename == "":
        print(line)
        return
    with open(output_filename, "a") as output_file:
        output_file.write(line)
        output_file.write('\n')

# TODO print code should be in UI
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
                if string_searches(easton_class.get_name(), and_strings, or_strings, not_strings) and \
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
    now = datetime.datetime.now()
    print_line("Data retrieved on {}".format(now.strftime("%b %d %Y %I:%M%P")), output_file)
