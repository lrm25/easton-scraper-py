from data.boulder_gym import BoulderGym
from data.easton_class import EastonClass
import storage.db as db

from .boulder_calendar import BoulderCalendar

def retrieve_boulder_classes():
    
    boulder_gym = BoulderGym()
    boulder_calendar = BoulderCalendar()
    boulder_calendar.get_and_parse_data(boulder_gym)
    easton_classes = boulder_gym.get_classes()
    for easton_class in easton_classes:
        print("{}, {}, {}, {}, {}".format(
            easton_class.get_id(),
            easton_class.get_name(), 
            easton_class.get_start_time(),
            easton_class.get_end_time(),
            easton_class.get_instructor()))
        db.write(easton_class)

def print_boulder_classes():
    db.load()
