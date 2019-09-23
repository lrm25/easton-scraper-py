from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from urllib.request import urlopen, Request

from data.easton_class import easton_class_sort, EastonClass
import data.easton_gym as easton_gym


class BoulderCalendar:

    def request(self, url):
        request = Request(url, headers={'User-Agent': 'lmccrone'})
        data = urlopen(request)
        soup = BeautifulSoup(data, "html.parser")
        return soup

    def get_and_parse_gyms_data(self, boulder_gym, first_class_date, number_of_days):

        gyms = [easton_gym.ARVADA, easton_gym.BOULDER, easton_gym.CENTENNIAL, easton_gym.AURORA, easton_gym.DENVER,
                easton_gym.LITTLETON]
        for gym in gyms:
            self.get_and_parse_data(gym[1], gym[3], boulder_gym, first_class_date, number_of_days)

    def get_and_parse_data(self, gym_name, gym_url, boulder_gym, first_class_date, number_of_days):

        for day_offset in range(number_of_days):
            self.get_and_parse_single_day(gym_name, gym_url, boulder_gym, first_class_date + timedelta(days=day_offset))

    def get_and_parse_single_day(self, gym_name, gym_url, boulder_gym, class_date):

        class_date_str = class_date.strftime("%Y-%m-%d")
        soup = self.request(gym_url)
        schedule_id = soup.find_all('healcode-widget')[0]['data-widget-id']
        # mindbody_url = "https://widgets.healcode.com/widgets/schedules/{}/print".format(schedule_id)
        mindbody_url = "https://widgets.healcode.com/widgets/schedules/{}/print?options%5Bstart_date%5D={}".format(
            schedule_id, class_date)
        print(mindbody_url)
        mindbody_page_data = self.request(mindbody_url)
        table_rows = mindbody_page_data.find_all('tr')
        for table_row in table_rows:
            if 'hc_class' in table_row.get('class'):
                name = table_row.find('span', {'class': 'classname'}).text.strip()

                start_time = table_row.find('span', {'class': 'hc_starttime'}).text.strip()
                parsed_start_time = datetime.strptime("{} {}".format(class_date_str, start_time), "%Y-%m-%d %I:%M %p")
                end_time = table_row.find('span', {'class': 'hc_endtime'}).text.replace("-", "").strip()
                parsed_end_time = datetime.strptime("{} {}".format(class_date_str, end_time), "%Y-%m-%d %I:%M %p")

                instructor = table_row.find('span', {'class': 'trainer'}).text.strip()

                if gym_name == 'Littleton':
                    class_id = table_row.get('data-bw-widget-mbo-class-id')
                else:
                    class_id = table_row.get('data-hc-mbo-class-id')

                easton_class = EastonClass(gym_name, class_id, name, class_date_str, start_time, end_time)
                easton_class.set_instructor(instructor)
                easton_class.set_sortable_start_time(parsed_start_time)
                easton_class.set_sortable_end_time(parsed_end_time)
                boulder_gym.add_class(easton_class)

        boulder_gym.get_classes().sort(key=easton_class_sort())
