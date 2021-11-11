"""
Module for the database class, MongoDB is used here.
"""
import os

import pymongo
from dotenv import load_dotenv
from scraper.utils import is_id_present

ALL_RECIPES = 0
FAVOURITES = 1
ATTRIBUTES = {'id', 'image url', 'yields', 'prep time', 'cook time', 'meal types', 'name',
              'description', 'ingredients', 'instructions', 'popularity'}


class Database:
    """
    Database class that stores the database and tables using mongoDB.
    Support update and insert to the database.
    Check errors if document to insert is not valid.
    """

    def __init__(self):
        """
        Connect to database and initialize tables
        """
        load_dotenv()
        self.client = pymongo.MongoClient(os.getenv('HOST'), os.getenv('PORT'))
        self.food_recipe_db = self.client['FoodRecipes']
        self.all_recipes_tb = self.food_recipe_db.all_recipes_table
        self.favourites_tb = self.food_recipe_db.favourites_table

    def is_recipe_exists_in_tb(self, recipe_dict, table_type):
        """
        Check whether recipe exists in all_recipes_table or favourites_table
        """
        recipe_id = recipe_dict['id']
        if table_type == ALL_RECIPES:
            recipe_info = self.all_recipes_tb.find_one({'id': recipe_id})
        if table_type == FAVOURITES:
            recipe_info = self.favourites_tb.find_one({'id': recipe_id})
        if recipe_info:
            return True
        return False

    def update_on_tb(self, recipe_dict, table_type):
        """
        Update the table by recipe_dict

        Parameters:
        recipe_dict (dict): dict of recipe to update
        table (int): flag indicating the type of table in database, all_recipes_tb or favourites_tb
        """
        if not is_id_present(recipe_dict):
            print('Error: id is not found')
            return False
        # return False if recipe_dict not exists in table, cannot update
        if not self.is_recipe_exists_in_tb(recipe_dict, table_type):
            print('Cannot update table: recipe does not exist')
            return False
        recipe_id = recipe_dict['id']
        my_query = {'id': recipe_id}
        for attribute in recipe_dict.keys():
            # skip update id because id will not change
            if attribute == 'id':
                continue
            # check error of malformed data structure
            if attribute not in ATTRIBUTES:
                print(f'Malformed data structure: '
                      f'recipe with id {recipe_id} has invalid attribute {attribute}')
                continue
            if not recipe_dict[attribute]:
                print(f'Malformed data structure: '
                      f'recipe with id {recipe_id} has empty value for attribute {attribute}')
                continue
            # update valid attribute and value into food_recipes_table
            new_values = {'$set': {attribute: recipe_dict[attribute]}}
            if table_type == ALL_RECIPES:
                self.all_recipes_tb.update_one(my_query, new_values)
                print(f'{attribute} entry of recipe with id {recipe_id} '
                      f'in all recipes table is updated')
            if table_type == FAVOURITES:
                self.favourites_tb.update_one(my_query, new_values)
                print(f'{attribute} entry of recipe with id {recipe_id} '
                      f'in favourites table is updated')
        return True

    def insert_into_tb(self, recipe_dict, table_type):
        """
        Insert recipe_dict into the table

        Parameters:
        recipe_dict (dict): dict of recipe to insert
        table (int): flag indicating the type of table in database, all_recipes_tb or favourites_tb
        """
        if not is_id_present(recipe_dict):
            print('Error: id is not found')
            return False
        # return False if recipe_dict exists in table, cannot insert
        if self.is_recipe_exists_in_tb(recipe_dict, table_type):
            print('Cannot insert into table: recipe already exists')
            return False
        to_insert = {}
        for attribute in recipe_dict.keys():
            # insert valid attributes and values into dict to_insert
            if attribute in ATTRIBUTES and recipe_dict[attribute]:
                to_insert[attribute] = recipe_dict[attribute]
        # insert to_insert to table in database
        recipe_id = recipe_dict['id']
        if table_type == ALL_RECIPES:
            self.all_recipes_tb.insert_one(to_insert)
            print(f'recipe with id {recipe_id} is inserted into all recipes table')
        if table_type == FAVOURITES:
            self.favourites_tb.insert_one(to_insert)
            print(f'recipe with id {recipe_id} is inserted into favourites table')
        return True
