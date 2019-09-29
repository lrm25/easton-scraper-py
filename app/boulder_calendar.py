from datetime import date, datetime, timedelta

from data.easton_class import EastonClass
import data.easton_gym as eg
from data.easton_gym import EastonGym
from storage import db

from . import html_request, zen_calendar


class BoulderCalendar:

    def get_and_parse_gyms_data(self, first_class_date, gyms_queried, number_of_days):

        gyms = [eg.ARVADA, eg.BOULDER, eg.CENTENNIAL, eg.AURORA, eg.DENVER,
                eg.LITTLETON, eg.CASTLE_ROCK, eg.THORNTON]
        for gym in gyms:
            if not len(gyms_queried) or gym[0].lower().replace(" ", "") in gyms_queried:
                easton_gym = EastonGym(gym)
                eg.gym_dict[easton_gym.get_name()] = easton_gym
                self.get_and_parse_data(easton_gym, first_class_date, number_of_days)

    def get_and_parse_data(self, gym, first_class_date, number_of_days):

        for day_offset in range(number_of_days):
            gym_type = gym.get_type()
            if gym_type == eg.MINDBODY:
                self.get_and_parse_single_day(gym, first_class_date + timedelta(days=day_offset))
            elif gym_type == eg.ZEN:
                zen_calendar.get_calendar_daily_data(gym, first_class_date + timedelta(days=day_offset))

    def get_and_parse_single_day(self, gym, class_date):

        # TODO fix, date is displaying everything within 24 hours of current moment
        class_date_str = class_date.strftime("%Y-%m-%d")
        soup = html_request.request(gym.get_url())
        schedule_id = soup.find_all('healcode-widget')[0]['data-widget-id']
        # mindbody_url = "https://widgets.healcode.com/widgets/schedules/{}/print".format(schedule_id)
        mindbody_url = "https://widgets.healcode.com/widgets/schedules/{}/print?options%5Bstart_date%5D={}".format(
            schedule_id, class_date)
        print(mindbody_url)
        mindbody_page_data = html_request.request(mindbody_url)
        table_rows = mindbody_page_data.find_all('tr')
        for table_row in table_rows:
            if 'hc_class' in table_row.get('class'):
                name_block = table_row.find('span', {'class': 'classname'})
                name = name_block.text.strip()
                description_link = name_block.find('a').get('data-url')

                start_time = table_row.find('span', {'class': 'hc_starttime'}).text.strip()
                parsed_start_time = datetime.strptime("{} {}".format(class_date_str, start_time), "%Y-%m-%d %I:%M %p")
                end_time = table_row.find('span', {'class': 'hc_endtime'}).text.replace("-", "").strip()
                parsed_end_time = datetime.strptime("{} {}".format(class_date_str, end_time), "%Y-%m-%d %I:%M %p")

                instructor = table_row.find('span', {'class': 'trainer'}).text.strip()

                if gym.get_name() == 'Littleton':
                    class_id = table_row.get('data-bw-widget-mbo-class-id')
                else:
                    class_id = table_row.get('data-hc-mbo-class-id')

                easton_class = EastonClass(gym.get_name(), class_id, name, class_date_str, start_time, end_time)
                easton_class.set_instructor(instructor)
                easton_class.set_sortable_start_time(parsed_start_time)
                easton_class.set_sortable_end_time(parsed_end_time)
                if 'cancelled' in table_row.get('class'):
                    easton_class.set_cancelled(True)
                easton_class.set_description_link(description_link)
                gym.add_class(easton_class)
                db.write(easton_class)


def get_class_description(description_link):

    description = ""
    soup = html_request.request(description_link)
    divs = soup.find_all('div')
    for div in divs:
        div_class = div.get('class')
        if div_class is not None and 'class_description' in div_class:
            for div_description in div:
                # character 194 shows up for some reason
                description = "{}\n{}".format(description, div_description.text.replace(chr(194), ""))
            break
    return description
