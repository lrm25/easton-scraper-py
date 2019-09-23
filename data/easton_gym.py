# Gym calendars
MINDBODY = 1
ZEN = 2

# Gym IDs
ARVADA = (1, 'Arvada', MINDBODY, "https://eastonbjj.com/arvada/schedule")
AURORA = (2, 'Aurora', MINDBODY, "https://eastonbjj.com/aurora/schedule")
BOULDER = (3, 'Boulder', MINDBODY, "https://eastonbjj.com/boulder/schedule")
CASTLE_ROCK = (4, 'Castle Rock', ZEN)
CENTENNIAL = (5, 'Centennial', MINDBODY, "https://eastonbjj.com/centennial/schedule")
DENVER = (6, 'Denver', MINDBODY, "https://eastonbjj.com/denver/schedule")
LITTLETON = (7, 'Littleton', MINDBODY, "https://eastonbjj.com/littleton/schedule")
THORNTON = (8, 'Thornton', ZEN)


class EastonGym:

    def __init__(self, gym_id):
        self._gym_id = gym_id
