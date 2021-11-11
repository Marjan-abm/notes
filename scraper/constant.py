"""
Module to store constant variables
"""
# url for the Fatsecret website
BASE_URL = 'https://www.fatsecret.com'
# url for random scrape
DEFAULT_URL = 'https://www.fatsecret.com/Default.aspx?pa=rs'
# part of url for scrape by meal type before the meal type
TYPE_URL_PRE = 'https://www.fatsecret.com/recipes/collections/meal/'
# part of url for scrape by meal type after the meal type
TYPE_URL_AFT = '/MostPopular.aspx'
# meal types to put between TYPE_URL_PRE and TYPE_URL_AFT
MEAL_TYPES = ['default', 'appetizer', 'bakery-and-baked-products', 'breakfast', 'dessert',
              'drinks-and-beverages', 'lunch', 'main-dish', 'salad',
              'sauces-condiments-and-dressings', 'side-dish', 'snack', 'soup']
# class names used in soup find during scraping
CLASS_NAME_DICT = {'default': {'table_class': 'listtable searchResult', 'td_class': 'borderBottom'},
                   'meal_type': {'table_class': 'listtable',
                                 'td_class': 'borderBottom recipeSummary'}}
# option values used in menu
OPTION_EXIT = 'q'
OPTION_BACK = 'b'
ZERO = 0
OPTION_ONE = 1
OPTION_TWO = 2
OPTION_THREE = 3
OPTION_FOUR = 4
OPTION_FIVE = 5
OPTION_SIX = 6
OPTION_SEVEN = 7
OPTION_EIGHT = 8
OPTION_NINE = 9
OPTION_TEN = 10
OPTION_ELEVEN = 11
OPTION_TWELVE = 12
