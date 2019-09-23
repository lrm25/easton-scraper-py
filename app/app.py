import calendar
from datetime import date, timedelta

from data.boulder_gym import BoulderGym
import storage.db as db

from .boulder_calendar import BoulderCalendar


def convert_weekday_to_days_ahead(weekday):
    day_list = [day_name.lower() for day_name in list(calendar.day_name)]
    try:
        day_index = day_list.index(weekday)
    except ValueError as e:
        return -1
    day_index += 7
    return day_index - date.today().weekday()


def retrieve_boulder_classes(class_date, number_of_days):
    
    boulder_gym = BoulderGym()
    boulder_calendar = BoulderCalendar()
    boulder_calendar.get_and_parse_gyms_data(boulder_gym, class_date, number_of_days)
    easton_classes = boulder_gym.get_classes()
    for easton_class in easton_classes:
        print("{}, {}, {}, {}, {}, {}, {}".format(
            easton_class.get_gym_name(),
            easton_class.get_id(),
            easton_class.get_name(),
            easton_class.get_date(),
            easton_class.get_start_time(),
            easton_class.get_end_time(),
            easton_class.get_instructor()))
        db.write(easton_class)


def print_boulder_classes(class_start_date, number_of_days):
    class_day_list = []
    for day_offset in range(number_of_days):
        offset_date = class_start_date + timedelta(day_offset)
        class_day_list.append(offset_date.strftime("%Y-%m-%d"))
    db.load(class_day_list)
