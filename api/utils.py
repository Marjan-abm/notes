"""
Utils module for api
"""
from flask import request


def is_content_type_json():
    """
    Check whether content type header is application/json
    """
    if request.content_type.startswith('application/json'):
        return True
    return False


def is_dict_value_type_valid(dic):
    """
    Check whether value type of the dict is string or list,
    and whether fields supposed to store number indeed store number.

    Parameters:
    dic (dict): dictionary given to check its value type
    """
    for key in dic:
        # value should be str or list
        if not isinstance(dic[key], str) and not isinstance(dic[key], list):
            return False
        # value of these keys should be int
        if key in {'yields', 'prep time', 'cook time', 'popularity'}:
            if not dic[key].isnumeric():
                return False
    return True
