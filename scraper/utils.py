"""
Module for the utils.
Methods here may be used repeatedly.
"""
import json
import re
from bson.json_util import dumps


def json_file_to_dict(json_file):
    """
    Read json file and return the content if it is a dict

    Parameters:
    json_file (str): address of json file to read
    """
    # get the content
    with open(json_file, 'r') as file:
        try:
            content = json.load(file)
        except ValueError:
            print('Invalid JSON file: File given is not a valid JSON file')
            return None
    if not content:
        return None
    # handle invalid content if not a dict
    if not isinstance(content, dict):
        print('Malformed data structure: Content of JSON file is not a dict')
        return None
    # return content as a dict
    return content


def export_to_json_file(mongo_db):
    """
    Export existing recipes into JSON files from database.
    JSON file name is 'recipes.json'

    Parameters:
    mongo_db (obj): instance of Database
    """
    if not mongo_db:
        print('Error: mongo_db given is None')
        return
    dictionary = {'all recipes': [], 'favourites': []}
    # get recipes in all_recipes_tb
    for recipe_info in mongo_db.all_recipes_tb.find({}, {'_id': 0}):
        recipe_info_dict = json.loads(dumps(recipe_info))
        dictionary['all recipes'].append(recipe_info_dict)
    # get recipes in favourites_tb
    for recipe_info in mongo_db.favourites_tb.find({}, {'_id': 0}):
        recipe_info_dict = json.loads(dumps(recipe_info))
        dictionary['favourites'].append(recipe_info_dict)
    # write to json file
    with open('recipes.json', 'w') as output_file:
        json.dump(dictionary, output_file, indent=4)
        print('Export successful: recipes are stored in recipes.json')


def update_by_json_file(mongo_db, json_file, table_type):
    """
    Update the database by json file

    Parameters:
    mongo_db (obj): Database instance
    json_file (str): address of json file
    table_type (int): flag indicating the type of table in database, all_recipes_tb or favourites_tb
    """
    if not mongo_db:
        print('Error: mongo_db given is None')
        return
    # get the content
    recipe_dict = json_file_to_dict(json_file)
    if not recipe_dict:
        return
    # update database by content
    mongo_db.update_on_tb(recipe_dict, table_type)


def insert_by_json_file(mongo_db, json_file, table_type):
    """
    Insert into the database by json file

    Parameters:
    mongo_db (obj): Database instance
    json_file (str): address of json file
    table_type (int): flag indicating the type of table in database, all_recipes_tb or favourites_tb
    """
    if not mongo_db:
        print('Error: mongo_db given is None')
        return
    # get the content
    recipe_dict = json_file_to_dict(json_file)
    if not recipe_dict:
        return
    # insert content into database
    mongo_db.insert_into_tb(recipe_dict, table_type)


def is_id_present(my_dict):
    """
    check if id is present in my dict with int value
    """
    if 'id' in my_dict.keys() and my_dict['id'].isnumeric():
        return True
    return False
