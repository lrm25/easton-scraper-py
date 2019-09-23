from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


class BoulderGym:

    def __init__(self):
        self._url = "https://eastonbjj.com/boulder/schedule"
        self._classes = []

    def get_url(self):
        return self._url

    def add_class(self, easton_class):
        self._classes.append(easton_class)

    def get_classes(self):
        return self._classes
