# Gym calendar types
MINDBODY = 1
ZEN = 2

# Gym tuple indices
IDX_TAG_NAME = 0
IDX_NAME = 1
IDX_CALENDAR_TYPE = 2
IDX_CALENDAR_URL = 3

# Gym indices
IDX_ARVADA = 0
IDX_AURORA = 1
IDX_BOULDER = 2
IDX_CENTENNIAL = 3
IDX_DENVER = 4
IDX_LITTLETON = 5
IDX_LONGMONT = 6
IDX_THORNTON = 7

# Gym data retrieval info tuples
GYM_TUPLES = [
    ('arvada', 'Arvada', MINDBODY, "https://eastonbjj.com/arvada/schedule"),
    ('aurora', 'Aurora', MINDBODY, "https://eastonbjj.com/aurora/schedule"),
    ('boulder', 'Boulder', MINDBODY, "https://eastonbjj.com/boulder/schedule"),
    #('castlerock', 'Castle Rock', ZEN, "https://etc-castlerock.sites.zenplanner.com/calendar.cfm"),
    ('centennial', 'Centennial', MINDBODY, "https://eastonbjj.com/centennial/schedule"),
    ('denver', 'Denver', MINDBODY, "https://eastonbjj.com/denver/schedule"),
    ('littleton', 'Littleton', MINDBODY, "https://eastonbjj.com/littleton/schedule"),
    ('longmont', 'Longmont', MINDBODY, "https://eastonbjj.com/longmont/schedule"),
    ('thornton', 'Thornton', ZEN, "https://eastonbjjnorth.sites.zenplanner.com/calendar.cfm")
    ]

# Attribute used to retrieve numerical class ID for Mindbody calendars (some were different in the past,
# but as of Jul 14 2020 this isn't the case)
mindbody_class_id = {
    'arvada': 'data-bw-widget-mbo-class-id',
    'aurora': 'data-bw-widget-mbo-class-id',
    'boulder': 'data-bw-widget-mbo-class-id',
    'centennial': 'data-bw-widget-mbo-class-id',
    'denver': 'data-bw-widget-mbo-class-id',
    'littleton': 'data-bw-widget-mbo-class-id',
    'longmont': 'data-bw-widget-mbo-class-id'
}

gym_tuple_idx_map = {}

# Allows external modules to retrieve gym objects
gym_dict = {}


#
# fill so that tuples can be retrieved by tag name as well as index
#
def create_tuple_map():
    for tuple in GYM_TUPLES:
        gym_tuple_idx_map[tuple[IDX_TAG_NAME]] = tuple


#
# Sort easton classes by start time, then end time, to organize class display
#
def easton_class_sort():
    return lambda e: (e.get_sortable_start_time(), e.get_sortable_end_time())


#
# Class representing Easton gym, containing info to retrieve classes, as well as retrieved class info from the internet
# or from local disk, if already retrieved and stored previously.
#
class EastonGym:

    def __init__(self, gym_tuple):
        self._name = gym_tuple[IDX_NAME]
        self._db_name = gym_tuple[IDX_TAG_NAME]
        self._type = gym_tuple[IDX_CALENDAR_TYPE]
        self._url = gym_tuple[IDX_CALENDAR_URL]
        self._classes = []

    def get_name(self):
        return self._name

    def get_db_name(self):
        return self._db_name

    def get_type(self):
        return self._type

    def get_url(self):
        return self._url

    def get_classes(self, date=None):
        if not date:
            return self._classes
        classes_on_date = []
        for easton_class in self._classes:
            if easton_class.get_date() == date:
                classes_on_date.append(easton_class)
        return classes_on_date

    def add_class(self, easton_class):
        self._classes.append(easton_class)

    def sort_classes(self):
        self._classes.sort(key=easton_class_sort())

