from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlopen, Request

from data.boulder_gym import BoulderGym
from data.easton_class import easton_class_sort, EastonClass

class BoulderCalendar:

    def request(self, url):
        request = Request(url, headers={'User-Agent': 'lmccrone'})
        data = urlopen(request)
        soup = BeautifulSoup(data, "html.parser")
        return soup

    def get_and_parse_data(self, boulder_gym):

        soup = self.request(boulder_gym.get_url())
        schedule_id = soup.find_all('healcode-widget')[0]['data-widget-id']
        mindbody_url = "https://widgets.healcode.com/widgets/schedules/{}/print".format(schedule_id)
        mindbody_page_data = self.request(mindbody_url)
        table_rows = mindbody_page_data.find_all('tr')
        for table_row in table_rows:
            if 'hc_class' in table_row.get('class'):

                name = table_row.find('span', {'class': 'classname'}).text.strip()

                start_time = table_row.find('span', {'class': 'hc_starttime'}).text.strip()
                parsed_start_time = datetime.strptime(start_time, "%I:%M %p")
                end_time = table_row.find('span', {'class': 'hc_endtime'}).text.replace("-", "").strip()
                parsed_end_time = datetime.strptime(end_time, "%I:%M %p")

                instructor = table_row.find('span', {'class': 'trainer'}).text.strip()

                class_id = table_row.get('data-hc-mbo-class-id')

                easton_class = EastonClass(class_id, name, start_time, end_time)
                easton_class.set_instructor(instructor)
                easton_class.set_sortable_start_time(parsed_start_time)
                easton_class.set_sortable_end_time(parsed_end_time)
                boulder_gym.add_class(easton_class)

        boulder_gym.get_classes().sort(key=easton_class_sort())