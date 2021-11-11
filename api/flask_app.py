"""
Web api using flask which supports GET, PUT, POST, DELETE.
Error message and HTTP status code (200, 400, 415, 404) is returned if error occurs in web api.
Only error message is returned if functions in this file is used in other local files.
"""
import json

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from bson.json_util import dumps

from scraper.database import Database, ALL_RECIPES, FAVOURITES
from scraper.scraper import scrape_food_recipe_page, get_starting_url_soup

from api.utils import is_content_type_json, is_dict_value_type_valid
from api.query import query, MALFORMED_QUERY_STRING, OBJECT_NOT_EXIST, OBJECT_NOT_MATCH, \
    FIELD_NOT_EXIST, VALUE_TYPE_ERROR, OPERATOR_NOT_APPLICABLE

app = Flask(__name__)
CORS(app)
mongo_db = Database()

DEFAULT_INPUT = -1
OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404
UNSUPPORTED_MEDIA_TYPE = 415


# http://127.0.0.1:5000/api/food?id={attr_value}
@app.route('/api/food', methods=['GET'])
def get_all_recipe_by_id(id_input=DEFAULT_INPUT):
    """
    Get the recipe detail from all recipes table by id.

    Parameters:
    id_input (str): id of recipe given from local
    """
    return get_recipe_by_id(id_input, ALL_RECIPES)


# http://127.0.0.1:5000/api/favourite?id={attr_value}
@app.route('/api/favourite', methods=['GET'])
def get_favourite_recipe_by_id(id_input=DEFAULT_INPUT):
    """
    Get the recipe detail from favourite recipes table by id.

    Parameters:
    id_input (str): id of recipe given from local
    """
    return get_recipe_by_id(id_input, FAVOURITES)


def get_recipe_by_id(id_input, table_type):
    """
    Helper method for get the recipe detail by id.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such name is found.

    Parameters:
    name (str): name of recipe
    table_type (int): flag indicating type of table to search
    """
    # get id and determine the output method: to web or to local
    is_to_web = True
    if id_input != DEFAULT_INPUT:
        arg = id_input
        is_to_web = False
    else:
        arg = request.args.get('id')
    if not arg:
        return proceed_to_output({'GET error': f'Recipe id {arg} is not valid'}, BAD_REQUEST,
                                 is_to_web)
    recipe_id = arg

    # try to get recipes by id
    recipe_doc = None
    if table_type == ALL_RECIPES:
        recipe_doc = mongo_db.all_recipes_tb.find_one({'id': recipe_id}, {'_id': 0})
    if table_type == FAVOURITES:
        recipe_doc = mongo_db.favourites_tb.find_one({'id': recipe_id}, {'_id': 0})
    # no recipe is found, return with error
    if not recipe_doc:
        return proceed_to_output({'GET error': f'Recipes with id {recipe_id} is not found'},
                                 NOT_FOUND, is_to_web)
    # get recipe dict from recipe_doc
    recipe_dict = json.loads(dumps(recipe_doc))
    # return to web or local
    return proceed_to_output(recipe_dict, OK, is_to_web)


# http://127.0.0.1:5000/api/search?q={query_string} Example: /search?q=all.id:123
@app.route('/api/search', methods=['GET'])
def get_by_query(query_string_input=DEFAULT_INPUT):
    """
    Get search results based on the specified query string.
    Errors should be reported if invalid search query.

    Parameters:
    query_string_input (str): query string for api given from local
    """
    # get query string and determine the output method: to web or to local
    is_to_web = True
    if query_string_input != DEFAULT_INPUT:
        query_string = query_string_input
        is_to_web = False
    else:
        query_string = request.args.get('q')
    # Parse and execute query string and get result documents
    documents = query(query_string, mongo_db)
    # Handle all the errors
    if documents is None:
        return proceed_to_output({'GET error': 'Result is not found in database'},
                                 NOT_FOUND, is_to_web)
    if documents == MALFORMED_QUERY_STRING:
        return proceed_to_output({'GET error': 'Malformed query strings'}, BAD_REQUEST, is_to_web)
    if documents == OBJECT_NOT_EXIST:
        return proceed_to_output({'GET error': 'Object in json does not exist'}, BAD_REQUEST,
                                 is_to_web)
    if documents == OBJECT_NOT_MATCH:
        return proceed_to_output({'GET error': 'Objects in json do not match'}, BAD_REQUEST,
                                 is_to_web)
    if documents == FIELD_NOT_EXIST:
        return proceed_to_output({'GET error': 'Field in json does not exist'}, BAD_REQUEST,
                                 is_to_web)
    if documents == VALUE_TYPE_ERROR:
        return proceed_to_output({'GET error': 'Value type of the field should be integer'},
                                 BAD_REQUEST, is_to_web)
    if documents == OPERATOR_NOT_APPLICABLE:
        return proceed_to_output({'GET error': 'Comparison operators not applicable for string'},
                                 BAD_REQUEST, is_to_web)
    if documents.count() == 0:
        return proceed_to_output({'GET error': 'Result is not found in database'},
                                 NOT_FOUND, is_to_web)
    # Process output
    res = []
    for doc in documents:
        res.append(json.loads(dumps(doc)))
    return proceed_to_output(res, OK, is_to_web)


# http://127.0.0.1:5000/api/food?id={attr_value}
@app.route('/api/food', methods=['PUT'])
def put_to_all_recipe_by_id(id_input=DEFAULT_INPUT, json_file_input=DEFAULT_INPUT):
    """
    Put, or update recipe specified by the ID.
    Call helper function put_recipe_by_id.

    Parameters:
    id_input (str): recipe id for api given from local
    json_file_input (str): json file for api given from local
    """
    return put_recipe_by_id(id_input, json_file_input, ALL_RECIPES)


# http://127.0.0.1:5000/api/favourite?id={attr_value}
@app.route('/api/favourite', methods=['PUT'])
def put_to_favourite_recipe_by_id(id_input=DEFAULT_INPUT, json_file_input=DEFAULT_INPUT):
    """
    Put, or update author specified by the ID.
    Call helper function put_recipe_by_id.

    Parameters:
    id_input (str): recipe id for api given from local
    json_file_input (str): json file for api given from local
    """
    return put_recipe_by_id(id_input, json_file_input, FAVOURITES)


def put_recipe_by_id(id_input, json_file_input, table_type):
    """
    Helper method for put recipe specified by the ID.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    id_input (str): recipe id for api given from local
    json_file_input (str): json file for api given from local
    table_type (int): flag indicating the type of table to update
    """
    # get id and determine the output method: to web or to local
    is_to_web = True
    if id_input != DEFAULT_INPUT:
        arg = id_input
        is_to_web = False
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'PUT error': f'Recipe id {arg} is not valid'}, BAD_REQUEST,
                                 is_to_web)
    recipe_id = arg

    # try to find recipe by id from table
    recipe_doc = None
    if table_type == ALL_RECIPES:
        recipe_doc = mongo_db.all_recipes_tb.find_one({'id': recipe_id}, {'_id': 0})
    if table_type == FAVOURITES:
        recipe_doc = mongo_db.favourites_tb.find_one({'id': recipe_id}, {'_id': 0})
    # recipe with id is not found, return with error
    if not recipe_doc:
        return proceed_to_output({'PUT error': f'Recipe with id {recipe_id} is not found'},
                                 NOT_FOUND, is_to_web)
    # Load json content from correct position
    if json_file_input != DEFAULT_INPUT:
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, is_to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'PUT error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, is_to_web)
        json_content = request.json
    # get recipe dict from json content
    recipe_dict = json.loads(dumps(json_content))
    # json content is not a dict, return with error
    if not isinstance(recipe_dict, dict):
        return proceed_to_output({'JSON structure error': 'Content of json is not a dict'},
                                 BAD_REQUEST, is_to_web)
    # value of dict is not valid, return with error
    if not is_dict_value_type_valid(recipe_dict):
        return proceed_to_output({'JSON value type error': 'Incorrect value type in json'},
                                 BAD_REQUEST, is_to_web)
    recipe_dict['id'] = recipe_id
    # update the table
    mongo_db.update_on_tb(recipe_dict, table_type)
    return proceed_to_output({'PUT success': f'Recipe with id {recipe_id} is updated'}, OK,
                             is_to_web)


# http://127.0.0.1:5000/api/food
@app.route('/api/food', methods=['POST'])
def post_to_all_recipe(json_file_input=DEFAULT_INPUT):
    """
    Leverage POST requests to ADD book to the all recipes table.
    Call helper function post_recipe.

    Parameters:
    json_file_input (str): json file for api given from local
    """
    return post_recipe(json_file_input, ALL_RECIPES)


# http://127.0.0.1:5000/api/favourite
@app.route('/api/favourite', methods=['POST'])
def post_to_favourite_recipe(json_file_input=DEFAULT_INPUT):
    """
    Leverage POST requests to ADD recipe to the favourite recipes table.
    Call helper function post_recipe.

    Parameters:
    json_file_input (str): json file for api given from local
    """
    return post_recipe(json_file_input, FAVOURITES)


def post_recipe(json_file_input, table_type):
    """
    Helper method for post to all/favourite recipes table.
    Leverage POST requests to ADD recipe to the backend (database).
    Error should be reported with HTTP status code BAD_REQUEST if id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    json_file_input (str): json file for api given from local
    table_type (int): flag indicating the type of table to update
    """
    to_web = True
    # Get json content
    if json_file_input != DEFAULT_INPUT:
        to_web = False
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'POST error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    # ready for service
    response_dict = {}
    recipe_dict = json.loads(dumps(json_content))
    # handle all the errors with error message
    if not isinstance(recipe_dict, dict):
        # If JSON is not a dict, error
        response_dict['JSON structure error'] = 'Content of json is not a dict'
        return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    if not is_dict_value_type_valid(recipe_dict):
        # If dict value is not valid, error
        response_dict['JSON content error'] = 'Incorrect value type in json'
        return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    if 'id' not in recipe_dict.keys():
        # If 'id' is not found in dict keys, error
        response_dict['JSON structure error'] = 'Found recipe dict with no id'
        return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    recipe_id = recipe_dict['id']
    if not recipe_id:
        # If 'id' is empty, error
        response_dict['POST input error'] = 'Invalid recipe id'
        return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    if table_type == ALL_RECIPES:
        if mongo_db.is_recipe_exists_in_tb(recipe_dict, ALL_RECIPES):
            # If value of 'id' already exists, error
            response_dict['POST input error'] = f'Recipe with id {recipe_id} already exists ' \
                                                f'in all recipes table'
            return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    if table_type == FAVOURITES:
        if mongo_db.is_recipe_exists_in_tb(recipe_dict, FAVOURITES):
            # If value of 'id' already exists, error
            response_dict['POST input error'] = f'Recipe with id {recipe_id} already exists ' \
                                                f'in favourite recipes table'
            return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    # insert recipe into specified table
    mongo_db.insert_into_tb(recipe_dict, table_type)
    response_dict['POST success'] = f'Recipe with id {recipe_id} is inserted'
    return proceed_to_output(response_dict, OK, to_web)


# http://127.0.0.1:5000/api/scrape?url={attr_value}
@app.route('/api/scrape', methods=['POST'])
def post_scrape(url_input=DEFAULT_INPUT):
    """
    Scrape food recipe and save the results in the database.
    Error should be reported with HTTP status code BAD_REQUEST if id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.
    URL parameters should be valid recipe page.

    Parameters:
    url_input (str): starting url for api given from local
    """
    to_web = True
    if url_input != DEFAULT_INPUT:
        to_web = False
        arg = url_input
    else:
        arg = request.args.get('url')
    url_str = arg
    # ready for service
    response_dict = {}
    if get_starting_url_soup(url_str):
        # url given is valid, scrape recipe page
        recipe_dict = scrape_food_recipe_page(url_str)
        if not recipe_dict:
            # recipe scrape error
            response_dict['POST scrape error'] = 'Recipe url given cannot be scraped'
            return proceed_to_output(response_dict, NOT_FOUND, to_web)
        recipe_id = recipe_dict['id']
        if mongo_db.is_recipe_exists_in_tb(recipe_dict, ALL_RECIPES):
            # recipe with id already exists, cannot insert
            response_dict['POST input error'] = f'Recipe with id {recipe_id} already exists'
            return proceed_to_output(response_dict, BAD_REQUEST, to_web)
        # insert into all recipes table
        mongo_db.insert_into_tb(recipe_dict, ALL_RECIPES)
        response_dict['POST success'] = f'Recipe with id {recipe_id} is inserted'
    else:
        # url invalid
        response_dict['POST error'] = 'URL is not a valid recipe page of FatSecret'
        return proceed_to_output(response_dict, BAD_REQUEST, to_web)
    return proceed_to_output(response_dict, OK, to_web)


# http://127.0.0.1:5000/api/book?id={attr_value} Example: /book?id=3735293
@app.route('/api/food', methods=['DELETE'])
def delete_from_all_recipe_by_id(id_input=DEFAULT_INPUT):
    """
    Delete recipe from all recipes table specified by the ID.
    Call helper function delete_recipe_by_id.

    Parameters:
    id_input (str): recipe id for api given from local
    """
    return delete_recipe_by_id(id_input, ALL_RECIPES)


# http://127.0.0.1:5000/api/author?id={attr_value} Example: /author?id=45372
@app.route('/api/favourite', methods=['DELETE'])
def delete_from_favourite_recipe_by_id(id_input=DEFAULT_INPUT):
    """
    Delete recipe from favourite recipes table specified by the ID.
    Call helper function delete_recipe_by_id.

    Parameters:
    id_input (str): recipe id for api given from local
    """
    return delete_recipe_by_id(id_input, FAVOURITES)


def delete_recipe_by_id(id_input, table_type):
    """
    Helper method for Delete recipe specified by the ID.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.

    Parameters:
    id_input (str): recipe id for api given from local
    table_type (int): flag indicating the type of table to update
    """
    is_to_web = True
    if id_input != DEFAULT_INPUT:
        is_to_web = False
        arg = id_input
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'DELETE error': f'Recipe id {arg} is not valid'},
                                 BAD_REQUEST, is_to_web)
    recipe_id = arg
    # try to find recipe by id
    if table_type == ALL_RECIPES:
        recipe_doc = mongo_db.all_recipes_tb.find_one({'id': recipe_id}, {'_id': 0})
    if table_type == FAVOURITES:
        recipe_doc = mongo_db.favourites_tb.find_one({'id': recipe_id}, {'_id': 0})
    # recipe does not exist
    if not recipe_doc:
        return proceed_to_output({'DELETE error': f'Recipe with id {recipe_id} is not found'},
                                 NOT_FOUND, is_to_web)
    # delete recipe with id
    if table_type == ALL_RECIPES:
        mongo_db.all_recipes_tb.delete_one({'id': recipe_id})
    if table_type == FAVOURITES:
        mongo_db.favourites_tb.delete_one({'id': recipe_id})
    return proceed_to_output({'DELETE success': f'Recipe with id {recipe_id} is deleted'}, OK,
                             is_to_web)


def proceed_to_output(response, status, is_to_web):
    """
    Return make_response if to_web is True, used in web api.
    Return a dict if to_web is False, used in local file.

    Parameters:
    response (dict): dictionary of response
    status (int): HTTP status code
    to_web (bool): whether the function should make response to web
    """
    if is_to_web:
        return make_response(jsonify(response), status)
    return response


if __name__ == '__main__':
    app.run(debug=True)
