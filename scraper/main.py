"""
Module for the main of scraper.
Contains the menu in terminal and process the user input.
"""
import sys

from scraper.constant import DEFAULT_URL, TYPE_URL_PRE, TYPE_URL_AFT, MEAL_TYPES, OPTION_EXIT, \
    OPTION_BACK, ZERO, OPTION_ONE, OPTION_TWO, OPTION_THREE, OPTION_FOUR, OPTION_FIVE, OPTION_SIX, \
    OPTION_SEVEN, OPTION_TWELVE
from scraper.scraper import scrape_many, scrape_one
from scraper.database import Database, ALL_RECIPES, FAVOURITES
from scraper.utils import export_to_json_file, update_by_json_file, insert_by_json_file
from api.menu_crud import menu_simulate_api


UPDATE = 0
INSERT = 1


def show_menu():
    """
    Show the tree-like menu and read user option
    """
    # Read user input using command line
    while True:
        choice = input('\nChoose one of the following options:\n'
                       '1 = Scrape food recipes randomly\n'
                       '2 = Scrape food recipes by meal type\n'
                       '3 = Scrape one food recipe by starting url\n'
                       '4 = Export existing recipes to json file\n'
                       '5 = Update by json file\n'
                       '6 = Insert by json file\n'
                       '7 = Simulate CRUD requests\n'
                       'q = EXIT\n\n')
        if choice == OPTION_EXIT:
            sys.exit(0)
        if not choice.isnumeric():
            continue
        option = int(choice)
        if OPTION_ONE <= option <= OPTION_SEVEN:
            break

    # Handle different options
    if option == OPTION_ONE:
        # 1 = Scrape food recipes randomly
        menu_scrape_many(True)
    if option == OPTION_TWO:
        # 2 = Scrape food recipes by meal type
        menu_scrape_many(False)
    if option == OPTION_THREE:
        # 3 = Scrape one food recipe by starting url
        menu_scrape_one()
    if option == OPTION_FOUR:
        # 4 = Export existing recipes to json file
        # set database
        global MONGO_DB
        if not MONGO_DB:
            MONGO_DB = Database()
        # export
        export_to_json_file(MONGO_DB)
        show_menu()
    if option == OPTION_FIVE:
        # 5 = Update by json file
        menu_update_insert_by_json_file(UPDATE)
    if option == OPTION_SIX:
        # 6 = Insert by json file
        menu_update_insert_by_json_file(INSERT)
    if option == OPTION_SEVEN:
        # 7 = Simulate CRUD requests
        menu_simulate_api()
        show_menu()


def menu_scrape_many(is_default):
    """
    menu to scrape specified number of recipes randomly or by meal type

    Parameters:
    is_default (bool): flag indicating whether to scrape randomly or by meal type
    """
    if not is_default:
        while True:
            choice = input('\nChoose one of the following options:\n'
                           '1 = Scrape appetizer\n'
                           '2 = Scrape bakery and baked products\n'
                           '3 = Scrape breakfast\n'
                           '4 = Scrape dessert\n'
                           '5 = Scrape drinks and beverages\n'
                           '6 = Scrape lunch\n'
                           '7 = Scrape main dish\n'
                           '8 = Scrape salad\n'
                           '9 = Scrape sauces condiments and dressings\n'
                           '10 = Scrape side dish\n'
                           '11 = Scrape snack\n'
                           '12 = Scrape soup\n'
                           'b = GO BACK\n\n')
            if choice == OPTION_BACK:
                show_menu()
                return
            if not choice.isnumeric():
                continue
            meal_type_choice = int(choice)
            if OPTION_ONE <= meal_type_choice <= OPTION_TWELVE:
                break

    while True:
        choice = input('\nChoose one of the following options:\n'
                       '<int> = number of food recipes to scrape\n'
                       'b = GO BACK\n\n')
        if choice == OPTION_BACK:
            if is_default:
                show_menu()
            else:
                menu_scrape_many(is_default)
            return
        if not choice.isnumeric():
            continue
        target_number = int(choice)
        if target_number >= ZERO:
            break

    if is_default:
        scrape_many(DEFAULT_URL, target_number, 'default')
    else:
        scrape_many(TYPE_URL_PRE + MEAL_TYPES[meal_type_choice] + TYPE_URL_AFT, target_number,
                    'meal_type')
    show_menu()


def menu_scrape_one():
    """
    menu to scrape one recipe by starting url
    """
    while True:
        choice = input('\nChoose one of the following options:\n'
                       '<str> = Starting url of a food recipe page\n'
                       'b = GO BACK\n\n')
        if choice == OPTION_BACK:
            show_menu()
            return
        if not choice:
            continue
        break
    scrape_one(choice)
    show_menu()


def menu_update_insert_by_json_file(operation):
    """
    menu for update/insert table by json file

    Parameters:
    operation (int): flag indicating the operation type from update/insert
    """
    # get the type of table to update
    while True:
        if operation == UPDATE:
            choice = input('\nChoose one of the following options:\n'
                           '1 = Update all recipes table\n'
                           '2 = Update favourite recipes table\n'
                           'b = GO BACK\n\n')
        if operation == INSERT:
            choice = input('\nChoose one of the following options:\n'
                           '1 = Insert all recipes table\n'
                           '2 = Insert favourite recipes table\n'
                           'b = GO BACK\n\n')
        if choice == OPTION_BACK:
            show_menu()
            return
        if not choice.isnumeric():
            continue
        option = int(choice)
        if OPTION_ONE <= option <= OPTION_TWO:
            break
    # get the json file address
    while True:
        json_file = input('\nChoose one of the following options:\n'
                          '<str> = address of json file\n'
                          'b = GO BACK\n\n')
        if json_file == OPTION_BACK:
            menu_update_insert_by_json_file(operation)
            return
        if not json_file:
            continue
        break

    # set database
    global MONGO_DB
    if not MONGO_DB:
        MONGO_DB = Database()

    # Handle different options
    if option == OPTION_ONE:
        # all recipes table
        if operation == UPDATE:
            # 1 = Update all recipes table
            update_by_json_file(MONGO_DB, json_file, ALL_RECIPES)
        if operation == INSERT:
            # 1 = Insert all recipes table
            insert_by_json_file(MONGO_DB, json_file, ALL_RECIPES)
    if option == OPTION_TWO:
        # favourite recipes table
        if operation == UPDATE:
            # 2 = Update favourite recipes table
            update_by_json_file(MONGO_DB, json_file, FAVOURITES)
        if operation == INSERT:
            # 2 = Insert favourite recipes table
            insert_by_json_file(MONGO_DB, json_file, FAVOURITES)
    show_menu()


if __name__ == '__main__':
    MONGO_DB = None
    print('Hello! Welcome to the food recipes collector.')
    show_menu()
