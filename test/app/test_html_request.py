from bs4 import BeautifulSoup
from mock import patch
import unittest
from urllib.error import URLError

from easton_scraper_py.app.html_request import get_html_data, request


dummy_soup = "kjdslajfsjfldkasfdjasdlkdjfdafjdasdf"


def mock_get_html_data(url, timeout):
    return dummy_soup


class TestTest(unittest.TestCase):

    # Time out (if 5.5.5.5 becomes valid, this will have to change)
    def test_get_html_data_1(self):
        self.assertRaises(URLError, get_html_data, "https://5.5.5.5", timeout=5)

    # Refused
    def test_get_html_data_2(self):
        self.assertRaises(URLError, get_html_data, "https://127.0.0.2")

    # Refused (return None)
    def test_request1(self):
        self.assertEqual(request("https://127.0.0.2"), None)

    # Gibberish soup
    @patch('easton_scraper_py.app.html_request.get_html_data', mock_get_html_data)
    def test_request2(self):
        self.assertEqual(request("https://dontcare"), BeautifulSoup(dummy_soup, "html.parser"))


if __name__ == "__main__":
    unittest.main()
