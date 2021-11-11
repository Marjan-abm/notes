"""
This module is used to parse query string and execute query finding in database.
Program supports the following query string:
. operator to specify a field of an object. For example, all.prep time
: operator to specify if a field contains search words. For example, all.prep time:20
AND, OR, and NOT logical operators. For example, all.prep time: NOT 10 AND all.cook time: 40
One-side unbounded comparison operators >, <. For example, all.cook time: > 30
"""
from scraper.database import ATTRIBUTES

ALL_RECIPES_STR = 'all'
FAVOURITE_RECIPES_STR = 'fav'
LOGICAL_OPERATORS = ['AND', 'OR']
LOGICAL_OPERATOR_SIGNS = ['$and', '$or']
COMPARISON_OPERATORS = ['<', '>']
COMPARISON_OPERATOR_SIGNS = ['$lt', '$gt']
BOOK_QUERY = 2
AUTHOR_QUERY = 3
NOT_EXIST = -1
CAN_BE_COMPARED = 1
CANNOT_BE_COMPARED = 0
MALFORMED_QUERY_STRING = -1
OBJECT_NOT_EXIST = -2
OBJECT_NOT_MATCH = -3
FIELD_NOT_EXIST = -4
VALUE_TYPE_ERROR = -5
OPERATOR_NOT_APPLICABLE = -6


def query(query_string, mongo_db):
    """
    Query the database and return cursor according to the query.
    If error happens during the process, then related error is returned.

    Parameters:
    query_string (str): query string for search
    mongo_db (object): database object
    """
    has_logical_operator = False
    # check if query string contain logical operator
    for operator in LOGICAL_OPERATORS:
        if query_string.find(operator) != NOT_EXIST:
            has_logical_operator = True
    if has_logical_operator:
        # need to first divide at AND/OR, then parse
        res = divide_query_string_and_parse(query_string)
    else:
        # parse directly
        res = parse_single_query(query_string)
    # check error
    if is_error_occur(res):
        return res
    # process the query in table and return cursor
    query_obj, my_query = res
    if query_obj == ALL_RECIPES_STR:
        return mongo_db.all_recipes_tb.find(my_query, {'_id': 0})
    return mongo_db.favourites_tb.find(my_query, {'_id': 0})


def divide_query_string_and_parse(query_string):
    """
    Divide query string into two query at AND/OR.
    Then parse the query separately.
    Check error after calling each helper functions.

    Parameters:
    query_string (str): query string for search
    """
    for i, logical_operator in enumerate(LOGICAL_OPERATORS):
        if query_string.find(logical_operator) != NOT_EXIST:
            obj_to_query = ''
            condition_list = []
            query_list = query_string.split(logical_operator)
            for curr_query in query_list:
                curr_query = curr_query.strip()
                # separate curr_query in str format obj.field:content into three parts
                parts = parser(curr_query)
                if is_error_occur(parts):
                    return parts
                curr_obj, curr_field, curr_content = parts
                # check if current obj part exists. i.e. either 'all' or 'fav'
                if curr_obj not in (ALL_RECIPES_STR, FAVOURITE_RECIPES_STR):
                    return OBJECT_NOT_EXIST
                # check if all obj part are the same
                if not obj_to_query:
                    # initialize obj_to_query
                    obj_to_query = curr_obj
                else:
                    # check if match, return OBJECT_NOT_MATCH error if not
                    if obj_to_query != curr_obj:
                        return OBJECT_NOT_MATCH
                # check if field exists, return FIELD_NOT_EXIST error if not
                if curr_field not in ATTRIBUTES:
                    return FIELD_NOT_EXIST
                # find query condition by combining field and content
                curr_condition = field_content_to_query(curr_field, curr_content)
                if is_error_occur(curr_condition):
                    return curr_condition
                condition_list.append(curr_condition)
            # process the query
            my_query = {LOGICAL_OPERATOR_SIGNS[i]: condition_list}
            return obj_to_query, my_query


def parse_single_query(query_string):
    """
    Parse the query directly.
    Check error after calling each helper functions.

    Parameters:
    query_string (str): query string for search
    """
    parts = parser(query_string)
    if is_error_occur(parts):
        return parts
    curr_obj, curr_field, curr_content = parts
    # check if current obj part exists. i.e. either 'all' or 'fav'
    if curr_obj not in (ALL_RECIPES_STR, FAVOURITE_RECIPES_STR):
        return OBJECT_NOT_EXIST
    # check if field exists, return FIELD_NOT_EXIST error if not
    if curr_field not in ATTRIBUTES:
        return FIELD_NOT_EXIST
    # find query condition by combining field and content
    curr_condition = field_content_to_query(curr_field, curr_content)
    if is_error_occur(curr_condition):
        return curr_condition
    # object is not valid
    return curr_obj, curr_condition


def parser(query_string):
    """
    Parse the query string and separate it by the format 'object.field:content' into three section.
    Error MALFORMED_QUERY_STRING is returned if '.' or ':' is not found.

    Parameters:
    query_string (str): query string for search
    """
    # Split once from .
    try:
        obj, rest_string = query_string.split('.', 1)
    except ValueError:
        return MALFORMED_QUERY_STRING
    # Split once from :
    try:
        field, content = rest_string.split(':', 1)
    except ValueError:
        return MALFORMED_QUERY_STRING
    return obj.strip(), field.strip(), content.strip()


def field_content_to_query(field, content):
    """
    Convert content section into query which is used in mongo_db.collection.find().
    NOT logical operators. For example, book.rating_count: NOT 123.
    One-side unbounded comparison operators <, >. For example, book.rating_count: > 123.
    Single content without operators. For example, book.book_id: 123.

    Parameters:
    field (str): field string in query string
    content (str): content string in query string
    """
    # NOT content
    if content.find('NOT') != NOT_EXIST:
        not_content = content.split('NOT')[1].strip()
        return {field: {'$ne': not_content}}
    # >, < content
    for i, operator in enumerate(COMPARISON_OPERATORS):
        if content.find(operator) != NOT_EXIST:
            com_content = content.split(operator)[1].strip()
            type_check = check_content_type(field, com_content)
            if is_error_occur(type_check):
                return type_check
            if type_check == CANNOT_BE_COMPARED:
                return OPERATOR_NOT_APPLICABLE
            return {'$expr': {COMPARISON_OPERATOR_SIGNS[i]: [{'$toInt': f'${field}'},
                                                             int(com_content)]}}
    # single content
    content = content.strip()
    type_check = check_content_type(field, content)
    if is_error_occur(type_check):
        return type_check
    if field in {'id', 'yields', 'prep time', 'cook time', 'popularity'}:
        # search for exact match
        return {field: content}
    # search for contain
    condition = {'$regex': '.*' + content + '.*'}
    return {field: condition}


def check_content_type(field, content):
    """
    Check the type of content corresponding to the field.
    If type of content is not correct, VALUE_TYPE_ERROR is returned.
    If type can be compared, return CAN_BE_COMPARED.
    Otherwise, return CANNOT_BE_COMPARED.

    Parameters:
    field (str): field string in query string
    content (str): content string in query string without operators
    """
    content = content.strip()
    if not content:
        return CANNOT_BE_COMPARED
    if field in {'id', 'yields', 'prep time', 'cook time', 'popularity'}:
        # Content value for these field should be integer
        if not content.isnumeric():
            return VALUE_TYPE_ERROR
        return CAN_BE_COMPARED
    # Value of other fields is not int, cannot be compared
    return CANNOT_BE_COMPARED


def is_error_occur(return_value):
    """
    Check whether error has occurred by the return value.

    Parameters:
    return_value: value returned from functions in this file
    """
    if isinstance(return_value, int) \
            and OPERATOR_NOT_APPLICABLE <= return_value <= MALFORMED_QUERY_STRING:
        return True
    return False
