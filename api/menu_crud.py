"""
This module is used to show menu and perform CRUD requests locally.
Input from user is handled and CRUD is simulated.
API functions from app file are called.
"""
from scraper.constant import OPTION_BACK, OPTION_ONE, OPTION_TWO, OPTION_THREE, OPTION_FOUR
from api.flask_app import get_all_recipe_by_id, get_favourite_recipe_by_id, get_by_query, \
    put_to_all_recipe_by_id, put_to_favourite_recipe_by_id, post_to_all_recipe, \
    post_to_favourite_recipe, post_scrape, delete_from_all_recipe_by_id, \
    delete_from_favourite_recipe_by_id


def menu_simulate_api():
    """
    Simulate web api in local.
    Show the menu and read user option, then go to the specified method.
    """
    while True:
        method = input("\nChoose method of api from one of the following:\n"
                       "1 = GET\n"
                       "2 = PUT\n"
                       "3 = POST\n"
                       "4 = DELETE\n"
                       "b = GO BACK\n\n")
        if method == OPTION_BACK:
            return
        if not method.isnumeric():
            continue
        method = int(method)
        if OPTION_ONE <= method <= OPTION_FOUR:
            break
    if method == OPTION_ONE:
        menu_get_api()
    if method == OPTION_TWO:
        menu_put_api()
    if method == OPTION_THREE:
        menu_post_api()
    if method == OPTION_FOUR:
        menu_delete_api()


def menu_get_api():
    """
    Perform api for GET locally
    """
    while True:
        option = input("\nChoose GET api from one of the following:\n"
                       "1 = api/food?id={attr_value}\n"
                       "2 = api/favourite?id={attr_value}\n"
                       "3 = api/search?q={query_string}\n"
                       "b = GO BACK\n\n")
        if option == OPTION_BACK:
            menu_simulate_api()
            return
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_THREE:
            break
    if option == OPTION_ONE:
        value = input("api/food?id=")
        print(get_all_recipe_by_id(value))
    if option == OPTION_TWO:
        value = input("api/favourite?id=")
        print(get_favourite_recipe_by_id(value))
    if option == OPTION_THREE:
        value = input("api/search?q=")
        print(get_by_query(value))


def menu_put_api():
    """
    Perform api for PUT locally
    """
    while True:
        option = input("\nChoose PUT api from one of the following:\n"
                       "1 = api/food?id={attr_value}\n"
                       "2 = api/favourite?id={attr_value}\n"
                       "b = GO BACK\n\n")
        if option == OPTION_BACK:
            menu_simulate_api()
            return
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_TWO:
            break
    if option == OPTION_ONE:
        value = input("api/food?id=")
        file = input("json file: ")
        print(put_to_all_recipe_by_id(value, file))
    if option == OPTION_TWO:
        value = input("api/favourite?id=")
        file = input("json file: ")
        print(put_to_favourite_recipe_by_id(value, file))


def menu_post_api():
    """
    Perform api for POST locally
    """
    while True:
        option = input("\nChoose POST api from one of the following:\n"
                       "1 = api/food\n"
                       "2 = api/favourite\n"
                       "3 = api/scrape?url={attr_value}\n"
                       "b = GO BACK\n\n")
        if option == OPTION_BACK:
            menu_simulate_api()
            return
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_THREE:
            break
    if option == OPTION_ONE:
        file = input("json file: ")
        print(post_to_all_recipe(file))
    if option == OPTION_TWO:
        file = input("json file: ")
        print(post_to_favourite_recipe(file))
    if option == OPTION_THREE:
        value = input("api/scrape?url=")
        print(post_scrape(value))


def menu_delete_api():
    """
    Perform api for DELETE locally
    """
    while True:
        option = input("\nChoose DELETE api from one of the following:\n"
                       "1 = api/food?id={attr_value}\n"
                       "2 = api/favourite?id={attr_value}\n"
                       "b = GO BACK\n\n")
        if option == OPTION_BACK:
            menu_simulate_api()
            return
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_TWO:
            break
    if option == OPTION_ONE:
        value = input("api/food?id=")
        print(delete_from_all_recipe_by_id(value))
    if option == OPTION_TWO:
        value = input("api/favourite?id=")
        print(delete_from_favourite_recipe_by_id(value))
