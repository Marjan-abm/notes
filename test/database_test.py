"""
Test module for database
"""
import unittest

from scraper.database import Database, ALL_RECIPES, FAVOURITES

RECIPE1 = {
            'id': '1',
            'name': 'Cake',
            'description': 'My Cake',
            'image url': 'https://m.ftscrt.com/static/recipe/d9f68f56.jpg',
            'yields': '1',
            'prep time': '1 mins',
            'cook time': '2 mins'
        }

RECIPE1_NEW = {
            'name': 'New Cake',
            'description': 'My New Cake',
            'image url': 'https://m.ftscrt.com/static/recipe/d9f68f56.jpg',
            'yields': '3',
            'prep time': '10 mins',
            'cook time': '20 mins',
            'meal types': [
                'Dessert'
            ],
            'ingredients': [
                'air',
                'magic'
            ],
            'instructions': [
                'First do this',
                'Then do this',
                'Be careful'
            ]
        }

RECIPE2 = {
            'id': '2',
            'name': 'Fruit Juice',
            'description': 'My Juice',
            'image url': 'https://m.ftscrt.com/static/recipe/d9f68f56.jpg',
            'yields': '1',
            'prep time': '5 mins',
            'meal types': [
                'drinks and beverages'
            ],
            'ingredients': [
                'water',
                'fruit'
            ],
            'instructions': [
                'Add water',
                'Add juice'
            ]
        }

RECIPE2_NEW = {
            'id': '2',
            'name': 'Magic Fruit Juice',
            'description': 'My Amazing Juice',
            'image url': 'https://m.ftscrt.com/static/recipe/d9f68f56.jpg',
            'yields': '1',
            'prep time': '5 mins',
            'meal types': [
                'drinks and beverages'
            ],
            'ingredients': [
                'water'
            ],
            'instructions': [
                'Add water',
                'Duang'
            ]
        }


class TestDatabase(unittest.TestCase):
    """
    Test class for database.
    Test all methods in this class.
    """

    def test_is_recipe_exists_all_recipes_tb(self):
        """
        Test method is_recipe_exists_in_tb
        """
        # Test for all_recipes_tb
        # test with no initial document
        self.assertFalse(MONGO_DB.is_recipe_exists_in_tb(RECIPE1, ALL_RECIPES))
        self.assertFalse(MONGO_DB.is_recipe_exists_in_tb(RECIPE2, ALL_RECIPES))

        # test after RECIPE1 is inserted
        MONGO_DB.all_recipes_tb.insert_one(RECIPE1)
        self.assertTrue(MONGO_DB.is_recipe_exists_in_tb(RECIPE1, ALL_RECIPES))
        self.assertFalse(MONGO_DB.is_recipe_exists_in_tb(RECIPE2, ALL_RECIPES))

        # Test for favourites_tb
        # test with no initial document
        self.assertFalse(MONGO_DB.is_recipe_exists_in_tb(RECIPE1, FAVOURITES))
        self.assertFalse(MONGO_DB.is_recipe_exists_in_tb(RECIPE2, FAVOURITES))

        # test after RECIPE2 is inserted
        MONGO_DB.favourites_tb.insert_one(RECIPE2)
        self.assertFalse(MONGO_DB.is_recipe_exists_in_tb(RECIPE1, FAVOURITES))
        self.assertTrue(MONGO_DB.is_recipe_exists_in_tb(RECIPE2, FAVOURITES))

        # delete all documents after test
        MONGO_DB.all_recipes_tb.delete_many({})
        MONGO_DB.favourites_tb.delete_many({})

    def test_update_on_tb(self):
        """
        Test method update_on_tb
        """
        # test update invalid dict will not insert
        MONGO_DB.update_on_tb(RECIPE1_NEW, ALL_RECIPES)
        self.assertEqual(None, MONGO_DB.all_recipes_tb.find_one({'id': '1'}))

        # test update invalid recipe dict
        MONGO_DB.all_recipes_tb.insert_one(RECIPE1)
        MONGO_DB.update_on_tb(RECIPE1_NEW, ALL_RECIPES)
        recipe1_dict = MONGO_DB.all_recipes_tb.find_one({'id': '1'})
        self.assertNotEqual(None, recipe1_dict)
        self.assertNotEqual('New Cake', recipe1_dict['name'])
        self.assertFalse('ingredients' in recipe1_dict.keys())

        # test update valid dict will not insert
        MONGO_DB.update_on_tb(RECIPE2_NEW, ALL_RECIPES)
        self.assertEqual(None, MONGO_DB.favourites_tb.find_one({'id': '1'}))

        # test update valid recipe dict
        MONGO_DB.favourites_tb.insert_one(RECIPE2)
        MONGO_DB.update_on_tb(RECIPE2_NEW, FAVOURITES)
        recipe2_dict = MONGO_DB.favourites_tb.find_one({'id': '2'})
        self.assertNotEqual(None, recipe1_dict)
        self.assertEqual('Magic Fruit Juice', recipe2_dict['name'])

        # delete all documents after test
        MONGO_DB.all_recipes_tb.delete_many({})
        MONGO_DB.favourites_tb.delete_many({})

    def test_insert_into_tb(self):
        """
        Test method insert_into_tb
        """
        # test insert invalid recipe dict
        MONGO_DB.all_recipes_tb.insert_one(RECIPE1_NEW)
        MONGO_DB.insert_into_tb(RECIPE1_NEW, ALL_RECIPES)
        recipe1_dict = MONGO_DB.all_recipes_tb.find_one({'id': '1'})
        self.assertEqual(None, recipe1_dict)

        # test insert valid recipe dict
        MONGO_DB.all_recipes_tb.insert_one(RECIPE2)
        MONGO_DB.insert_into_tb(RECIPE2, ALL_RECIPES)
        recipe1_dict = MONGO_DB.all_recipes_tb.find_one({'id': '2'})
        self.assertNotEqual(None, recipe1_dict)

        # delete all documents after test
        MONGO_DB.all_recipes_tb.delete_many({})


if __name__ == '__main__':
    MONGO_DB = Database()
    # delete all documents
    MONGO_DB.all_recipes_tb.delete_many({})
    MONGO_DB.favourites_tb.delete_many({})
    # run tests
    unittest.main()
