from aiohttp import ClientSession
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen, Request

#
# function that handles the actual URL request
#
async def get_html_data(url, timeout=60):
    async with ClientSession() as session:
        async with session.get(url, headers={'User-Agent': 'lrm25'}) as response:
            return await response.read()

#
# get and parse a html webpage
#
async def request(url, timeout=60):

    try:
        data = await get_html_data(url, timeout)
    except URLError as e:
        print("Error:  {}".format(e))
        return None

    soup = BeautifulSoup(data, "html.parser")
    return soup
