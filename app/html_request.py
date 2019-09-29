from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def request(url):
    request_handle = Request(url, headers={'User-Agent': 'lmccrone'})
    data = urlopen(request_handle)
    soup = BeautifulSoup(data, "html.parser")
    return soup
