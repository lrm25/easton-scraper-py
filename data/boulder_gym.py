from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

class BoulderGym:

    def __init__(self):
        self._url = "https://eastonbjj.com/boulder/schedule"

    def get_url(self):
        return self._url

    def parse_schedule_id(self, page_html_data):
        soup = BeautifulSoup(page_html_data, "html.parser")
        schedule_id = soup.find_all('healcode-widget')[0]['data-widget-id']
        return schedule_id