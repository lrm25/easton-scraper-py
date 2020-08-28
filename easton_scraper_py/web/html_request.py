from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen, Request


#
# function that handles the actual URL request
#
def get_html_data(url, timeout=60):

    request_handle = Request(url, headers={'User-Agent': 'lmccrone'})
    data = urlopen(request_handle, timeout=timeout)
    return data


#
# get and parse a html webpage
#
def request(url, timeout=60):

    try:
        data = get_html_data(url, timeout)
    except URLError as e:
        print("Error:  {}".format(e))
        return None

    soup = BeautifulSoup(data, "html.parser")
    return soup
