from bs4 import BeautifulSoup
from datetime import datetime
import mock
from mock import Mock, patch
import unittest

from app import mindbody_calendar

from data.easton_gym import EastonGym


def mock_request_no_healcode(url):
    return BeautifulSoup('dummy/easton-no-healcode.html', 'html.parser')


class MindbodyCalendarTest(unittest.TestCase):

    # no "healcode-widget"
    @patch('app.html_request.request', mock_request_no_healcode)
    @mock.patch('data.easton_gym.EastonGym')
    def test_get_and_parse_single_day1(self, mock_gym):
            mock_gym.get_url.return_value = "https://dontcare"
            mock_gym.get_name.return_value = "dummy gym"
            print(mock_gym.get_name())
            mindbody_calendar.get_and_parse_single_day(mock_gym, datetime.now())

