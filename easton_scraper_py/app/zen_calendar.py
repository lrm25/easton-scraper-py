from datetime import datetime, timedelta

from data.easton_class import EastonClass
from storage import db

from web import html_request


#
# Get Zen weekly calendar, return soup if dates match up
#
def retrieve_week_calendar_and_check_date(gym, date_string, offset_date):

    soup = html_request.request(gym.get_url() + "?DATE=" + date_string + "&VIEW=WEEK")

    # check week (only for ridiculous dates like one in the year 19 A.D.)
    week_description = soup.find('div', {'align': 'center'}).text.replace("Week of ", "")
    date_object = datetime.strptime(week_description, "%b %d, %Y")
    first_day_of_week = date_object.date()
    if offset_date < first_day_of_week or first_day_of_week + timedelta(days=7) <= offset_date:
        print("Error:  date {} is too far in the past".format(date_string))
        return None

    return soup


#
# Retrieve and parse an individual class
#
def parse_class(calendar_class, webpage_base, date_string, gym):

    name = calendar_class.text.strip()
    # Class info URL query is in single quotes in 'onclick' attribute
    # FORMAT:  onclick="checkLoggedId('enrollment.cfm?appointmentId=<id>')"
    class_link_attr = calendar_class.get('onclick')
    class_link_query = class_link_attr.split('\'')[1]
    class_id = class_link_query.split('?')[1].split('=')[1]
    class_link = "{}{}".format(webpage_base, class_link_query)
    class_soup = html_request.request(class_link)
    class_rows = class_soup.find_all('tr')
    instructor = "Staff"
    time_found = False
    staff_found = False
    start_time = ""
    end_time = ""
    sortable_start_time = None
    sortable_end_time = None
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

    if not time_found:
        print("Error:  class {} contains no time info".format(name))

    else:
        easton_class = EastonClass(gym.get_name(), gym.get_db_name(), class_id, name,
                                   date_string, start_time, end_time)
        easton_class.set_instructor(instructor)
        easton_class.set_sortable_start_time(sortable_start_time)
        easton_class.set_sortable_end_time(sortable_end_time)
        easton_class.set_description_link(class_link)
        gym.add_class(easton_class)
        db.write(easton_class)


#
# Scrape class data from gyms that use zencalendar
#
def get_calendar_daily_data(gym, first_date, number_of_days):

    soup = None
    retrieve_new_week = True

    for day_offset in range(number_of_days):
        offset_date = first_date + timedelta(days=day_offset)
        if not retrieve_new_week and offset_date.strftime().weekday() == 6:
            retrieve_new_week = True
        date_string = offset_date.strftime("%Y-%m-%d")
        if retrieve_new_week:
            soup = retrieve_week_calendar_and_check_date(gym, date_string, offset_date)
            if not soup:
                return

        print("Retrieving {} data for {} gym".format(date_string, gym.get_name()))
        day_schedule = soup.find('div', {'date': date_string})
        if not day_schedule:
            print("Error:  no calendar segment found on website for day {}".format(date_string))
            return

        calendar_classes = day_schedule.find_all('div', {'class': 'item'})
        # strip string "calendar.cfm" (12 chars)
        webpage_base = gym.get_url().replace("calendar.cfm", "")
        for calendar_class in calendar_classes:
            parse_class(calendar_class, webpage_base, date_string, gym)


#
# Get a class description from online, if available
#
def get_class_description(description_link):

    description = ""
    soup = html_request.request(description_link)
    divs = soup.find_all('div')
    for div in divs:
        # Identification:  div class="spaceBelow", no children
        div_class = div.get('class')
        if div_class is not None and 'spaceBelow' in div_class and not div.find('div'):
            description = div.text
            break
    if description == "":
        description = " *** No description given on website *** "
    return description

