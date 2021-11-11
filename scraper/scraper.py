"""
Module for the scraper.
Contain methods to scrape recipes in https://www.fatsecret.com
Storage into the database after every scrape.
Progress and error is reported during scraping.
"""
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from bs4 import BeautifulSoup

from scraper.constant import BASE_URL, CLASS_NAME_DICT
from scraper.database import Database, ALL_RECIPES

# control the number of dash in print for progress
DASH_NUMBER = 30


def get_soup(url):
    """
    Get the soup by url
    """
    try:
        html = urlopen(url)
    except HTTPError as err:
        print('Error: cannot open url')
        print('Error code: ', err.code)
        return None
    except URLError as err:
        print('Error: cannot open url')
        print('Reason: ', err.reason)
        return None
    return BeautifulSoup(html, 'html.parser')


def scrape_many(url, target_number, scrape_type):
    """
    Used to scrape many food recipe pages.
    First get all page links with list of food recipe links on them,
    then call scrape_all_rows method to scrape each page
    """
    soup = get_soup(url)
    if soup is None:
        return

    search_results_paging = soup.find('div', class_='searchResultsPaging')
    if not search_results_paging:
        print('Error: search page links not found')
        return

    rel_links_holder = search_results_paging.find_all('a')
    if not rel_links_holder:
        print('Error: search page links not found')
        return

    # init database
    mongo_db = Database()
    # init number of recipes left to scrape
    number_left = target_number
    # for every link to page that contains list of recipe links,
    # open the link and get the list of recipe links, then scrape
    for current_rel_url_holder in rel_links_holder:
        if number_left <= 0:
            break

        current_url = BASE_URL + current_rel_url_holder['href']
        soup = get_soup(current_url)
        if soup is None:
            return

        table = soup.find('table', class_=CLASS_NAME_DICT[scrape_type]['table_class'])
        if not table:
            print('Error: table not found')
            return

        rows = table.find_all('tr')
        if not rows:
            print('Error: rows not found')
            return
        # scrape all rows of recipe links
        count_success_scrape = scrape_all_rows(rows, number_left, target_number, scrape_type,
                                               mongo_db)
        number_left -= count_success_scrape


def scrape_all_rows(rows, number_left, target_number, scrape_type, mongo_db):
    """
    For each row of food recipe link on current page until target_number is reached,
    call scrape_food_recipe_page method to scrape all attributes
    """
    row_idx = 0
    count_success_scrape = 0
    # for every row in the page, find the link to the recipe page, then scrape
    for i in range(target_number - number_left, target_number):
        if row_idx >= len(rows):
            # no more rows of food recipe in current page
            break

        print('-' * DASH_NUMBER, f'Scraping food recipe {i + 1}/{target_number}', '-' * DASH_NUMBER)

        while row_idx < len(rows):
            rel_link = rows[row_idx].find('td', class_=CLASS_NAME_DICT[scrape_type]['td_class'])\
                .find('a')
            if not rel_link:
                # page link not found error
                print('Error: food recipe link not found')
                row_idx += 1
                continue

            food_recipe_url = BASE_URL + rel_link['href']
            food_recipe_dict = scrape_food_recipe_page(food_recipe_url)
            if not food_recipe_dict:
                # error in finding all attributes
                print('Error in scraping food recipe attributes')
                row_idx += 1
                continue
            # successfully get the food_recipe_dict
            count_success_scrape += 1
            break
        # store into database
        if mongo_db.is_recipe_exists_in_tb(food_recipe_dict, ALL_RECIPES):
            # exists, then update
            mongo_db.update_on_tb(food_recipe_dict, ALL_RECIPES)
        else:
            # not exist, then insert
            mongo_db.insert_into_tb(food_recipe_dict, ALL_RECIPES)
        row_idx += 1

    return count_success_scrape


def scrape_one(url):
    """
    Used to scrape one food recipe page
    """
    soup = get_starting_url_soup(url)
    if soup is None:
        print('Error: starting url is not a valid food recipe page')
        return
    food_recipe_dict = scrape_food_recipe_page(url)
    if not food_recipe_dict:
        # error in finding all attributes
        print('Error in scraping food recipe attributes')
        return
    # init database
    mongo_db = Database()
    # store into database
    if mongo_db.is_recipe_exists_in_tb(food_recipe_dict, ALL_RECIPES):
        # exists, then update
        mongo_db.update_on_tb(food_recipe_dict, ALL_RECIPES)
    else:
        # not exist, then insert
        mongo_db.insert_into_tb(food_recipe_dict, ALL_RECIPES)


def get_starting_url_soup(url):
    """
    First check if starting url is a valid food recipe page.
    If not, return None.
    Otherwise, return the soup.
    """
    if url[:34] != 'https://www.fatsecret.com/recipes/':
        return None
    if url.split('/')[-1] != 'Default.aspx':
        return None
    soup = get_soup(url)
    if not soup:
        return None
    table = soup.find('table', class_='generic')
    if not table:
        return None
    return soup


def scrape_food_recipe_page(url):
    """
    Scrape food recipes attributes
    """
    food_recipe_dict = {}
    soup = get_soup(url)
    if soup is None:
        return None

    table = soup.find('table', class_='generic')
    if not table:
        print('Error: table not found')
        return None

    # get id
    recipe_id = get_id(table)
    if recipe_id:
        food_recipe_dict['id'] = recipe_id
    else:
        # if no id, then stop scraping current recipe
        return None

    # get name
    name = get_name(table)
    if name:
        food_recipe_dict['name'] = name

    # get description
    description = get_description(table)
    if description:
        food_recipe_dict['description'] = description

    # get image url
    image_url = get_image_url(table)
    if image_url:
        food_recipe_dict['image url'] = image_url

    # get yields
    yields = get_yields(table)
    if yields:
        food_recipe_dict['yields'] = yields

    # get cook time and prep time
    prep_time, cook_time = get_time(table)
    if prep_time:
        food_recipe_dict['prep time'] = prep_time
    if cook_time:
        food_recipe_dict['cook time'] = cook_time

    # get meal types
    meal_types = get_meal_type(table)
    if meal_types:
        food_recipe_dict['meal types'] = meal_types

    # get ingredients
    ingredients = get_ingredients(table)
    if ingredients:
        food_recipe_dict['ingredients'] = ingredients

    # get instructions
    instructions = get_instructions(table)
    if instructions:
        food_recipe_dict['instructions'] = instructions

    # get popularity
    popularity = get_popularity(table)
    if popularity:
        food_recipe_dict['popularity'] = popularity

    return food_recipe_dict


def get_image_url(table):
    """
    get image url by table
    """
    img = table.find('img')
    if not img:
        print('Error: img not found')
        return None
    return img['src']


def get_yields(table):
    """
    get yields by table
    """
    servings = table.find(id='servings')
    if not servings:
        print('Error: servings not found')
    else:
        yield_div = servings.find('div', class_='yield')
        if not yield_div:
            print('Error: yield not found')
        else:
            return yield_div.text.strip().split(' ')[0]
    return None


def get_time(table):
    """
    get cook time and prep time by table
    """
    prep_time_mins = None
    cook_time_mins = None
    time_div = table.find(id='cooktime')
    if not time_div:
        print('Error: cook time not found')
    else:
        # prep time
        prep_time_div = time_div.find('div', class_='prepTime')
        if not prep_time_div:
            print('Error: prep time not found')
        else:
            prep_time = prep_time_div.text.strip()
            if prep_time[0] == '"':
                prep_time = prep_time[1:]
            if prep_time[-1] == '"':
                prep_time = prep_time[:-1]
            # get time from str
            res = prep_time.split(' ')
            if len(res) == 2:
                # get time from str format x mins OR x hr
                prep_time_mins = int(res[0])
                if res[1] == 'hr':
                    prep_time_mins = prep_time_mins * 60
            else:
                # get time from str format x hr y mins
                prep_time_mins = int(res[0]) * 60 + int(res[2])
            # convert from int to str
            prep_time_mins = str(prep_time_mins)

        # cook time
        cook_time_div = time_div.find('div', class_='cookTime')
        if not cook_time_div:
            print('Error: cook time not found')
        else:
            cook_time = cook_time_div.text.strip()
            if cook_time[0] == '"':
                cook_time = cook_time[1:]
            if cook_time[-1] == '"':
                cook_time = cook_time[:-1]
            # get time from str
            res = cook_time.split(' ')
            if len(res) == 2:
                # get time from str format x mins OR x hr
                cook_time_mins = int(res[0])
                if res[1] == 'hr':
                    cook_time_mins = cook_time_mins * 60
            else:
                # get time from str format x hr y mins
                cook_time_mins = int(res[0]) * 60 + int(res[2])
            # convert from int to str
            cook_time_mins = str(cook_time_mins)
    return prep_time_mins, cook_time_mins


def get_meal_type(table):
    """
    get meal types by table
    """
    meal_types = []
    meal_types_div = table.find(id='mealtypes')
    if not meal_types_div:
        print('Error: meal types not found')
    else:
        meal_types_container = meal_types_div.find_all('div', class_='tag')
        for meal_type_container in meal_types_container:
            meal_types.append(meal_type_container.text.strip())
    return meal_types


def get_name(table):
    """
    get the name of recipe by table
    """
    top_div = table.find('div', class_='top')
    if not top_div:
        print('Error: name not found')
    else:
        name_header = top_div.find('h1', class_='fn')
        if not name_header:
            print('Error: name not found')
        else:
            return name_header.text.strip()
    return None


def get_description(table):
    """
    get description of recipe by table
    """
    summary_span = table.find('span', class_='summary')
    if not summary_span:
        print('Error: summary not found')
        return None
    return summary_span.text.strip()


def get_ingredients(table):
    """
    get ingredients of recipe by table
    """
    ingredients = []
    ingredients_ul = table.find('ul', class_='plain ingredients')
    if not ingredients_ul:
        print('Error: ingredients not found')
    else:
        ingredients_container = ingredients_ul.find_all('li')
        for ingredient_container in ingredients_container:
            ingredients.append(ingredient_container.text.strip())
    return ingredients


def get_instructions(table):
    """
    get instructions of recipe by table
    """
    instructions = []
    instructions_ol = table.find('ol', class_='noind instructions')
    if not instructions_ol:
        print('Error: instructions not found')
    else:
        instructions_container = instructions_ol.find_all('li')
        for instruction_container in instructions_container:
            instructions.append(instruction_container.text.strip())
    return instructions


def get_popularity(table):
    """
    get popularity of recipe by table
    """
    popularity_div = table.find('div', class_='bluebg')
    if not popularity_div:
        print('Error: popularity not found')
        return None
    return popularity_div.text.strip().split(' ')[0]


def get_id(table):
    """
    Get the id of food recipe by table
    """
    img_frame_div = table.find('div', class_='imgFrame')
    if not img_frame_div:
        print('Error: id not found')
    else:
        id_holder = img_frame_div.find('a')
        if not id_holder:
            print('Error: id not found')
        else:
            url = id_holder['href'].strip()
            for i in range(len(url))[::-1]:
                if not url[i].isnumeric():
                    return url[i + 1:]
            return url
    return None
