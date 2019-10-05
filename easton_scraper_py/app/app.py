import calendar
from datetime import date, timedelta

from data import easton_gym
from data.easton_gym import EastonGym
import storage.db as db

from . import easton_calendar, mindbody_calendar, zen_calendar


def convert_weekday_to_days_ahead(weekday):

    day_list = [day_name.lower() for day_name in list(calendar.day_name)]
    try:
        day_index = day_list.index(weekday)
    except ValueError:
        return -1

    day_index += 7
    return day_index - date.today().weekday()


def delete_old_classes():

    db.delete_classes_done_before_now()


def retrieve_classes(class_date, gyms, number_of_days):
    
    easton_calendar.get_and_parse_gyms_data(class_date, gyms, number_of_days)


def load_classes(class_start_date, gyms, number_of_days):

    class_day_list = []
    for day_offset in range(number_of_days):
        offset_date = class_start_date + timedelta(day_offset)
        class_day_list.append(offset_date.strftime("%Y-%m-%d"))
    easton_classes = db.load(class_day_list)
    for easton_class in easton_classes:
        gym_name = easton_class.get_gym_name()
        if not len(gyms) or gym_name.replace(" ", "").lower() in gyms:
            try:
                gym = easton_gym.gym_dict[gym_name]
            except KeyError:
                gym = EastonGym(easton_gym.gym_tuple_dict[gym_name])
            gym.add_class(easton_class)
    for gym in easton_gym.gym_dict.values():
        gym.sort_classes()


def or_search(easton_class_name, or_strings):

    if not or_strings:
        return True
    for or_string in or_strings:
        if easton_class_name.find(or_string) != -1:
            return True
    return False


def not_search(easton_class_name, not_strings):
    if not not_strings:
        return True
    for not_string in not_strings:
        if easton_class_name.find(not_string) != -1:
            return False
    return True


def and_search(easton_class_name, and_strings):

    if not and_strings:
        return True
    for and_string in and_strings:
        if easton_class_name.find(and_string) == -1:
            return False
    return True


def string_searches(easton_class_name, and_strings, or_strings, not_strings):

    lowercase_name = easton_class_name.lower()
    return and_search(lowercase_name, and_strings) and or_search(lowercase_name, or_strings) and \
        not_search(lowercase_name, not_strings)


def get_class_description(gym_name, class_id):

    if gym_name == 'castlerock':
        gym_name = 'Castle_Rock'

    try:
        link = db.get_class_description_link(gym_name, class_id)
        if gym_name == 'Castle_Rock' or gym_name == 'Thornton':
            description = zen_calendar.get_class_description(link)
        else:
            description = mindbody_calendar.get_class_description(link)
        print(description)

    except ValueError as e:
        print(e)


def print_classes(class_start_date, number_of_days, and_strings, or_strings, not_strings,
                  instructor, no_cancelled, ids):

    matches = False
    for day_offset in range(number_of_days):
        day_match = False
        class_date_object = class_start_date + timedelta(days=day_offset)
        class_date = class_date_object.strftime("%Y-%m-%d")
        fancy_class_date = class_date_object.strftime("%A, %B %d, %Y")
        for gym in easton_gym.gym_dict.values():
            gym_match = False
            for easton_class in gym.get_classes(class_date):
                if string_searches(easton_class.get_name(), and_strings, or_strings, not_strings) and \
                   (instructor == "" or easton_class.get_instructor().lower().find(instructor) != -1) and \
                        not (easton_class.get_cancelled() and no_cancelled):
                    if not day_match:
                        print(" **** {} **** ".format(fancy_class_date))
                        day_match = True
                    if not gym_match:
                        print()
                        print(" **** {} **** ".format(gym.get_name()))
                        print()
                        gym_match = True
                        matches = True
                    print("{}, {}, {}, {}{}{}".format(easton_class.get_start_time(), easton_class.get_end_time(),
                          easton_class.get_name(), easton_class.get_instructor(),
                          ", {}".format(easton_class.get_id()) if ids else "",
                          ', CANCELLED' if easton_class.get_cancelled() else ""))
        if day_match:
            print()
            print()

    if not matches:
        print(" **** NO MATCHES **** ")
        print()
        print()
