from datetime import datetime, timedelta

from data.easton_class import EastonClass
from storage import db

from . import html_request


#
# Scrape class data from gyms that use zencalendar
#
# params:
# gym_location:  string representing gym location ("Castle Rock", etc.)
# webpage_location:  calendar webpage URL
# added_class_list:  reference to list of classes found over all gyms so far, function adds to this
#
def get_calendar_daily_data(gym, first_date):

    date_string = first_date.strftime("%Y-%m-%d")
    soup = html_request.request(gym.get_url()+"?DATE="+date_string+"&VIEW=WEEK")
    day_schedule = soup.find('div', {'date': date_string})
    calendar_classes = day_schedule.find_all('div', {'class': 'item'})
    # strip string "calendar.cfm" (12 chars)
    webpage_base = gym.get_url()[:-12]
    for calendar_class in calendar_classes:

        # Class info URL query is in single quotes in 'onclick' attribute
        # FORMAT:  onclick="checkLoggedId('enrollment.cfm?appointmentId=<id>')"
        class_link_attr = calendar_class.get('onclick')
        print("CLASS LINK ATTR: {}".format(class_link_attr))
        class_link_query = class_link_attr.split('\'')[1]
        class_id = class_link_query.split('?')[1].split('=')[1]
        class_soup = html_request.request("{}{}".format(webpage_base, class_link_query))
        class_rows = class_soup.find_all('tr')
        class_time = ""
        instructor = "Staff"
        time_found = False
        staff_found = False
        for class_row in class_rows:
            if class_row.find('td').text == 'Time':
                class_time = class_row.find('td', {'class': 'bold'}).text
                class_time_list = class_time.split(" - ")
                start_time = class_time_list[0]
                end_time = class_time_list[1]
                sortable_start_time = datetime.strptime("{} {}".format(date_string, start_time), "%Y-%m-%d %I:%M %p")
                sortable_end_time = datetime.strptime("{} {}".format(date_string, end_time), "%Y-%m-%d %I:%M %p")
                time_found = True
            if class_row.find('td').text == 'Staff':
                instructor = class_row.find_all('td')[1].text
                staff_found = True
            if time_found and staff_found:
                break

        easton_class = EastonClass(gym.get_name(), class_id, calendar_class.text.strip(), date_string, start_time, end_time)
        easton_class.set_instructor(instructor)
        easton_class.set_sortable_start_time(sortable_start_time)
        easton_class.set_sortable_end_time(sortable_end_time)
        gym.add_class(easton_class)
        db.write(easton_class)

