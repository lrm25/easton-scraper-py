from datetime import timedelta

from app import mindbody_calendar, zen_calendar
import data.easton_gym as eg
from data.easton_gym import EastonGym


#
# Get data for all gyms over day range
#
def get_and_parse_gyms_data(gyms_queried, first_class_date, number_of_days):

    for gym_tuple in eg.GYM_TUPLES:
        if not len(gyms_queried) or gym_tuple[eg.IDX_TAG_NAME] in gyms_queried:
            easton_gym = EastonGym(gym_tuple)
            eg.gym_dict[easton_gym.get_name()] = easton_gym
            get_and_parse_data(easton_gym, first_class_date, number_of_days)


#
# Get data for a single gym, over a period of a number of days
#
def get_and_parse_data(gym, first_class_date, number_of_days):

    gym_type = gym.get_type()
    if gym_type == eg.MINDBODY:
        for day_offset in range(number_of_days):
            mindbody_calendar.get_and_parse_single_day(gym, first_class_date + timedelta(days=day_offset))
    elif gym_type == eg.ZEN:
        zen_calendar.get_calendar_daily_data(gym, first_class_date, number_of_days)
    gym.sort_classes()
