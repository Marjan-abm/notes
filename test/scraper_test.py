"""
Test module for scrapers
"""
import unittest

from scraper.scraper import get_soup, get_id, get_name, get_time, get_yields, get_popularity, \
    get_description, get_ingredients, get_instructions, get_image_url, get_meal_type


class TestRecipeScraper(unittest.TestCase):
    """
    Test class for scrapers.
    Test methods that use soup.
    """

    def test_get_id(self):
        """
        Test method get_id
        """
        global TABLE_LIST
        self.assertEqual('52389300', get_id(TABLE_LIST[0]))
        self.assertEqual('23613877', get_id(TABLE_LIST[1]))

    def test_get_name(self):
        """
        Test method get_name
        """
        global TABLE_LIST
        self.assertEqual('Energy Bites', get_name(TABLE_LIST[0]))
        self.assertEqual('Low Carb Pancakes', get_name(TABLE_LIST[1]))

    def test_get_time(self):
        """
        Test method get_time
        """
        global TABLE_LIST
        prep0, cook0 = get_time(TABLE_LIST[0])
        self.assertEqual('15', prep0)
        self.assertEqual(None, cook0)
        prep1, cook1 = get_time(TABLE_LIST[1])
        self.assertEqual('5', prep1)
        self.assertEqual('5', cook1)

    def test_get_yields(self):
        """
        Test method get_yields
        """
        global TABLE_LIST
        self.assertEqual('6', get_yields(TABLE_LIST[0]))
        self.assertEqual('1', get_yields(TABLE_LIST[1]))

    def test_get_popularity(self):
        """
        Test method get_popularity
        """
        global TABLE_LIST
        self.assertEqual(None, get_popularity(TABLE_LIST[0]))
        self.assertEqual('10', get_popularity(TABLE_LIST[1]))

    def test_get_image_url(self):
        """
        Test method get_image_url
        """
        global TABLE_LIST
        self.assertEqual('https://m.ftscrt.com/static/recipe/173b952f-97bf-4ece-'
                         '987b-1887175b9285.jpg', get_image_url(TABLE_LIST[0]))
        self.assertEqual('https://m.ftscrt.com/static/recipe/41803aa7-98b2-4444-'
                         '9fd6-a27c55c95ca0.jpg', get_image_url(TABLE_LIST[1]))

    def test_get_description(self):
        """
        Test method get_description
        """
        global TABLE_LIST
        self.assertEqual('Cholesterol-free, no-bake treat.', get_description(TABLE_LIST[0]))
        self.assertEqual('Fits Ideal Protein Phase 1 protocol, on the cheap.',
                         get_description(TABLE_LIST[1]))

    def test_get_ingredients(self):
        """
        Test method get_ingredients
        """
        global TABLE_LIST
        self.assertEqual('1/4 cup dutch chocolate', get_ingredients(TABLE_LIST[0])[0])
        self.assertEqual('1/4 cup calorie free pancake syrup', get_ingredients(TABLE_LIST[1])[0])

    def test_get_instructions(self):
        """
        Test method get_instructions
        """
        global TABLE_LIST
        self.assertEqual('Grind oats in a food processor.', get_instructions(TABLE_LIST[0])[0])
        self.assertEqual('Preheat non-stick frying pan/griddle to medium-high heat with a '
                         'spritz of non-fat cooking spray.', get_instructions(TABLE_LIST[1])[0])

    def test_get_meal_type(self):
        """
        Test method get_meal_type
        """
        global TABLE_LIST
        self.assertEqual('Snacks', get_meal_type(TABLE_LIST[0])[0])
        self.assertEqual('Breakfast', get_meal_type(TABLE_LIST[1])[0])


if __name__ == '__main__':
    URL_LIST = ['https://www.fatsecret.com/recipes/52389300-energy-bites/Default.aspx',
                'https://www.fatsecret.com/recipes/low-carb-pancakes/Default.aspx']
    TABLE_LIST = []
    for url in URL_LIST:
        soup = get_soup(url)
        if soup:
            TABLE_LIST.append(soup.find('table', class_='generic'))
        else:
            TABLE_LIST.append(None)
    unittest.main()
