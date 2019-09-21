from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

from data.boulder_gym import BoulderGym

def get_boulder_schedule_id():
    
    boulder_gym = BoulderGym()
    easton_request = Request(boulder_gym.get_url(), headers={'User-Agent': "lmccrone"})
    schedule_page = urlopen(easton_request)
    return boulder_gym.parse_schedule_id(schedule_page)