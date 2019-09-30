# Gym calendars
MINDBODY = 1
ZEN = 2

# Gym tuples
ARVADA = ('Arvada', MINDBODY, "https://eastonbjj.com/arvada/schedule")
AURORA = ('Aurora', MINDBODY, "https://eastonbjj.com/aurora/schedule")
BOULDER = ('Boulder', MINDBODY, "https://eastonbjj.com/boulder/schedule")
CASTLE_ROCK = ('Castle Rock', ZEN, "https://etc-castlerock.sites.zenplanner.com/calendar.cfm")
CENTENNIAL = ('Centennial', MINDBODY, "https://eastonbjj.com/centennial/schedule")
DENVER = ('Denver', MINDBODY, "https://eastonbjj.com/denver/schedule")
LITTLETON = ('Littleton', MINDBODY, "https://eastonbjj.com/littleton/schedule")
THORNTON = ('Thornton', ZEN, "https://eastonbjjnorth.sites.zenplanner.com/calendar.cfm")

gym_tuple_dict = {
    'Arvada': ARVADA,
    'Aurora': AURORA,
    'Boulder': BOULDER,
    'Castle Rock': CASTLE_ROCK,
    'Centennial': CENTENNIAL,
    'Denver': DENVER,
    'Littleton': LITTLETON,
    'Thornton': THORNTON,
}

gym_dict = {}


def easton_class_sort():
    return lambda e: (e.get_sortable_start_time(), e.get_sortable_end_time())


class EastonGym:

    def __init__(self, gym_tuple):
        self._name = gym_tuple[0]
        self._type = gym_tuple[1]
        self._url = gym_tuple[2]
        self._classes = []
        gym_dict[self._name] = self

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_url(self):
        return self._url

    def get_classes(self):
        return self._classes

    def get_classes(self, date):
        classes_on_date = []
        for easton_class in self._classes:
            if easton_class.get_date() == date:
                classes_on_date.append(easton_class)
        return classes_on_date

    def add_class(self, easton_class):
        self._classes.append(easton_class)

    def sort_classes(self):
        self._classes.sort(key=easton_class_sort())

