import unittest
from unittest.mock import MagicMock
from processor import CoronavirusScraper, DataProcessor

class TestProcessor(unittest.TestCase):
    def test_fetch_covid_data(self):
        # Mock the fetch_covid_data function to return a known value
        CoronavirusScraper.fetch_covid_data = MagicMock(return_value="1,000,000")

        # Call the method that uses fetch_covid_data
        total_cases = CoronavirusScraper.fetch_covid_data()

        # Assert that the method returned the expected value
        self.assertEqual(total_cases, "1,000,000")

if __name__ == '__main__':
    unittest.main()
