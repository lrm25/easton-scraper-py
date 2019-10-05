from datetime import datetime

from data.easton_class import EastonClass
from storage import db

from . import html_request


#
# get the underlying mindbody widget ID so the easton calendar mindbody framework can be accessed
# class_date:  datetime object
#
def get_mindbody_widget_id(easton_calendar_url):

    easton_calendar_soup = html_request.request(easton_calendar_url)
    if not easton_calendar_soup:
        print("Error:  {} request returned error or empty page".format(easton_calendar_url))
        return None

    healcode_html_block = easton_calendar_soup.find('healcode-widget')
    if not healcode_html_block:
        print("Error:  {} request, unable to find 'healcode-widget' element".format(easton_calendar_url))
        return None

    widget_id = healcode_html_block.get('data-widget-id')
    if not widget_id:
        print("Error:  {} request, unable to find 'data-widget-id' attribute".format(easton_calendar_url))
        return None

    return widget_id


#
# Get mindbody calendar page data using mindbody widget ID in easton html
#
def get_mindbody_calendar_data(widget_id, class_date):

    mindbody_url = "https://widgets.healcode.com/widgets/schedules/{}/print?options%5Bstart_date%5D={}".format(
        widget_id, class_date)
    mindbody_page_data = html_request.request(mindbody_url)
    if not mindbody_page_data:
        print("Error retrieving mindbody page data with widget ID {}".format(widget_id))
    return mindbody_page_data


#
# Parse mindbody calendar data for a single gym, single day
#
def get_and_parse_single_day(gym, class_date):

    class_date_str = class_date.strftime("%Y-%m-%d")

    print("Retrieving {} data for {} gym".format(class_date_str, gym.get_name()))
    widget_id = get_mindbody_widget_id(gym.get_url())
    if not widget_id:
        print("Unable to retrieve class data for gym {} on {}".format(gym.get_name(), class_date_str))
        return

    mindbody_page_data = get_mindbody_calendar_data(widget_id, class_date)
    if not mindbody_page_data:
        print("Unable to retrieve mindbody calendar data for gym {} on {}".format(gym.get_name(), class_date_str))

    table_rows = mindbody_page_data.find_all('tr')
    for table_row in table_rows:
        # Identifier for easton class in data is 'hc_class'
        if 'hc_class' in table_row.get('class'):
            name_block = table_row.find('span', {'class': 'classname'})
            if not name_block:
                print("Error:  easton class marked with 'hc_class' contains no name")
                continue
            name = name_block.text.strip()

            description_block = name_block.find('a')
            if not description_block:
                print("Error:  easton class with name {} contains no description block".format(description_block))
                continue
            description_link = description_block.get('data-url')
            if not description_link:
                print("Error:  easton class with name {} contains no description link".format(description_block))
                continue

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
            if div.text != "":
                description = div.text.replace(chr(194), '\n')
            else:
                for div_description in div:
                    # character 194 shows up for some reason
                    description = "{}\n{}".format(description, div_description.text.replace(chr(194), ""))
                break
    if description == "":
        description = " *** No description given on website *** "
    return description
