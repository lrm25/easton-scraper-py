from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def getData():
    
    easton_request = Request("https://eastonbjj.com/boulder/schedule", headers={'User-Agent': "lmccrone"})
    schedule = urlopen(easton_request)
    print(schedule)
    soup = BeautifulSoup(schedule.read())
    print(soup)
    schedule_id = soup.find_all('healcode-widget')[0]['data-widget-id']
    print(schedule_id)