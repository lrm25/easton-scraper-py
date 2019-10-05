from datetime import timedelta

from app import mindbody_calendar, zen_calendar
import data.easton_gym as eg
from data.easton_gym import EastonGym


def get_and_parse_gyms_data(first_class_date, gyms_queried, number_of_days):

    gyms = [eg.ARVADA, eg.BOULDER, eg.CENTENNIAL, eg.AURORA, eg.DENVER,
            eg.LITTLETON, eg.CASTLE_ROCK, eg.THORNTON]
    for gym in gyms:
        if not len(gyms_queried) or gym[0].lower().replace(" ", "") in gyms_queried:
            easton_gym = EastonGym(gym)
            eg.gym_dict[easton_gym.get_name()] = easton_gym
            get_and_parse_data(easton_gym, first_class_date, number_of_days)


def get_and_parse_data(gym, first_class_date, number_of_days):

    for day_offset in range(number_of_days):
        gym_type = gym.get_type()
        if gym_type == eg.MINDBODY:
            mindbody_calendar.get_and_parse_single_day(gym, first_class_date + timedelta(days=day_offset))
        elif gym_type == eg.ZEN:
            zen_calendar.get_calendar_daily_data(gym, first_class_date + timedelta(days=day_offset))
    gym.sort_classes()
