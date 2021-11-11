"""
Test module for web api
"""
import unittest
import requests

from api.flask_app import mongo_db

BASE = 'http://127.0.0.1:5000/'


class TestApi(unittest.TestCase):
    """
    Test class for flask_app.py using api requests
    """

    def test_get_all_recipe_by_id(self):
        """
        Test method get_all_recipe_by_id
        """
        response = requests.get(BASE + 'api/food?id=52521158')
        self.assertEqual(404, response.status_code)

        json_content = {'id': '52521158', 'name': 'my food'}
        requests.post(BASE + 'api/food', json=json_content)

        response = requests.get(BASE + 'api/food?id=52521158')
        self.assertEqual(200, response.status_code)

        mongo_db.all_recipes_tb.delete_many({})

    def test_get_favourite_recipe_by_id(self):
        """
        Test method get_all_recipe_by_id
        """
        response = requests.get(BASE + 'api/favourite?id=6678')
        self.assertEqual(404, response.status_code)

        json_content = {'id': '6678', 'name': 'my food'}
        requests.post(BASE + 'api/favourite', json=json_content)

        response = requests.get(BASE + 'api/favourite?id=6678')
        self.assertEqual(200, response.status_code)

        mongo_db.favourites_tb.delete_many({})

    def test_get_by_query_basic(self):
        """
        Test method get_by_query
        """
        json_content = {'id': '1024', 'name': 'basic food'}
        requests.post(BASE + 'api/food', json=json_content)

        response = requests.get(BASE + 'api/search?q=id in all:1024')
        self.assertEqual(400, response.status_code)

        response = requests.get(BASE + 'api/search?q=dog.name:happy')
        self.assertEqual(400, response.status_code)

        response = requests.get(BASE + 'api/search?q=all.id:256')
        self.assertEqual(404, response.status_code)

        response = requests.get(BASE + 'api/search?q=all.id:1024')
        self.assertEqual(200, response.status_code)

        mongo_db.all_recipes_tb.delete_many({})

    def test_get_by_query_logical_operator(self):
        """
        Test method get_by_query
        """
        json_content1 = {'id': '4096', 'name': 'test logical operator food', 'yields': '3'}
        json_content2 = {'id': '5096', 'prep time': '10'}
        requests.post(BASE + 'api/food', json=json_content1)
        requests.post(BASE + 'api/food', json=json_content2)

        response = requests.get(BASE + 'api/search?q=all.name:test AND fav.name:no')
        self.assertEqual(400, response.status_code)

        response = requests.get(BASE + 'api/search?q=all.name:test AND all.yields:3AND all.id:4096')
        self.assertEqual(200, response.status_code)

        response = requests.get(BASE + 'api/search?q=all.name:none OR all.prep time: 10')
        self.assertEqual(200, response.status_code)

        response = requests.get(BASE + 'api/search?q=all.id:NOT 4096ANDall.id:NOT 5096')
        self.assertEqual(404, response.status_code)

        mongo_db.all_recipes_tb.delete_many({})

    def test_get_by_query_comparison_operator(self):
        """
        Test GET api/search?q={query_string} with
        one-side unbounded comparison operators <, >.
        """
        json_content1 = {'id': '8848', 'name': 'test compa 1', 'popularity': '5'}
        json_content2 = {'id': '9981', 'name': 'test compa 2', 'yields': '10', 'popularity': '2'}
        requests.post(BASE + 'api/favourite', json=json_content1)
        requests.post(BASE + 'api/favourite', json=json_content2)

        response = requests.get(BASE + 'api/search?q=fav.popularity:>4')
        self.assertEqual(200, response.status_code)

        response = requests.get(BASE + 'api/search?q=fav.popularity: < 1')
        self.assertEqual(404, response.status_code)

        response = requests.get(BASE + 'api/search?q=fav.name: > eee')
        self.assertEqual(400, response.status_code)

        mongo_db.favourites_tb.delete_many({})

    def test_put_to_all_recipe_by_id(self):
        """
        Test method put_to_all_recipe_by_id
        """
        json_content = {'id': '85009', 'name': 'wow'}
        requests.post(BASE + 'api/food', json=json_content)

        json_content = {'yields': '5', 'popularity': 'letter'}
        response = requests.put(BASE + 'api/food?id=85009', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = {'yields': '5', 'popularity': '10'}
        response = requests.put(BASE + 'api/food?id=85009', json=json_content)
        self.assertEqual(200, response.status_code)

        mongo_db.all_recipes_tb.delete_many({})

    def test_put_to_favourite_recipe_by_id(self):
        """
        Test method put_to_favourite_recipe_by_id
        """
        json_content = {'id': '85999', 'name': 'again'}
        requests.post(BASE + 'api/favourite', json=json_content)

        json_content = {'yields': '2', 'popularity': 'letter'}
        response = requests.put(BASE + 'api/favourite?id=85999', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = {'yields': '2', 'popularity': '5'}
        response = requests.put(BASE + 'api/favourite?id=85999', json=json_content)
        self.assertEqual(200, response.status_code)

        mongo_db.favourites_tb.delete_many({})

    def test_post_scrape(self):
        """
        Test method post_scrape
        """
        url = 'https://www.fatsecret.com/recipes/52521158-crepes/Default.aspx'
        response = requests.post(BASE + 'api/scrape?url=' + url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(mongo_db.all_recipes_tb.find_one({'id': '52521158'}))

        mongo_db.all_recipes_tb.delete_many({})

    def test_delete_from_all_recipe_by_id(self):
        """
        Test method delete_from_all_recipe_by_id
        """
        json_content = {'id': '52521158', 'name': 'my food'}
        requests.post(BASE + 'api/food', json=json_content)

        response = requests.get(BASE + 'api/food?id=52521158')
        self.assertEqual(200, response.status_code)

        response = requests.delete(BASE + 'api/food?id=52521158')
        self.assertEqual(200, response.status_code)

    def test_delete_from_favourite_recipe_by_id(self):
        """
        Test method delete_from_favourite_recipe_by_id
        """
        json_content = {'id': '6678', 'name': 'my food'}
        requests.post(BASE + 'api/favourite', json=json_content)

        response = requests.get(BASE + 'api/favourite?id=6678')
        self.assertEqual(200, response.status_code)

        response = requests.delete(BASE + 'api/favourite?id=6678')
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    mongo_db.all_recipes_tb.delete_many({})
    mongo_db.favourites_tb.delete_many({})
    unittest.main()
