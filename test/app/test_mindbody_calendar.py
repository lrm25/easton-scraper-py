from bs4 import BeautifulSoup
from datetime import datetime
import mock
from mock import Mock, patch
import unittest

from app import mindbody_calendar

from data.easton_gym import EastonGym


def mock_request_no_return(url):
    return None


def mock_request_no_healcode(url):
    with open('test/app/dummy/easton-no-healcode.html') as f:
        data = f.read()
    return BeautifulSoup(data, 'html.parser')


def mock_request_no_widget_id(url):
    with open('test/app/dummy/easton-no-data-widget-id.html') as f:
        data = f.read()
    return BeautifulSoup(data, 'html.parser')


class MindbodyCalendarTest(unittest.TestCase):

    # error retrieving any easton website data
    @patch('app.html_request.request', mock_request_no_return)
    @mock.patch('data.easton_gym.EastonGym')
    def test_get_mindbody_schedule_id1(self, mock_gym):
        mock_gym.get_url.return_value = "https://dontcare"
        mock_gym.get_name.return_value = "dummy gym"
        self.assertEqual(mindbody_calendar.get_and_parse_single_day(mock_gym, datetime.now()), None)

    # no "healcode-widget"
    @patch('app.html_request.request', mock_request_no_healcode)
    @mock.patch('data.easton_gym.EastonGym')
    def test_get_mindbody_schedule_id2(self, mock_gym):
        mock_gym.get_url.return_value = "https://dontcare"
        mock_gym.get_name.return_value = "dummy gym"
        self.assertEqual(mindbody_calendar.get_and_parse_single_day(mock_gym, datetime.now()), None)

    # healcode-widget has no 'data-widget-id' attribute
    @patch('app.html_request.request', mock_request_no_widget_id)
    @mock.patch('data.easton_gym.EastonGym')
    def test_get_mindbody_schedule_id3(self, mock_gym):
        mock_gym.get_url.return_value = "https://dontcare"
        mock_gym.get_name.return_value = "dummy gym"
        self.assertEqual(mindbody_calendar.get_and_parse_single_day(mock_gym, datetime.now()), None)

    # empty data return w/widget
    @patch('app.html_request.request', mock_request_no_return)
    def test_get_mindbody_calendar_data(self):
        self.assertEqual(mindbody_calendar.get_mindbody_calendar_data(None, None), None)
