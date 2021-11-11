"""
Test module for query
"""
import unittest

from api.query import parser, parse_single_query, divide_query_string_and_parse, check_content_type


class TestQuery(unittest.TestCase):
    """
    Test class for query.py
    """

    def test_parser(self):
        """
        Test method parser
        """
        invalid_q1 = 'all:name. hello'
        invalid_q2 = 'all.all.name = hello'
        valid_q1 = 'all.id: 555'
        valid_q2 = 'fav.   cook time: 33'
        self.assertEqual(-1, parser(invalid_q1))
        self.assertEqual(-1, parser(invalid_q2))
        self.assertEqual(('all', 'id', '555'), parser(valid_q1))
        self.assertEqual(('fav', 'cook time', '33'), parser(valid_q2))

    def test_parse_single_query(self):
        """
        Test method parse_single_query
        """
        invalid_q1 = 'all recipe.prep time: 222'
        invalid_q2 = 'fav.what: no'
        valid_q1 = 'all.id: 555'
        valid_q2 = 'fav.   cook time: NOT 33'
        self.assertEqual(-2, parse_single_query(invalid_q1))
        self.assertEqual(-4, parse_single_query(invalid_q2))
        self.assertEqual(('all', {'id': '555'}), parse_single_query(valid_q1))
        self.assertEqual(('fav', {'cook time': {'$ne': '33'}}), parse_single_query(valid_q2))

    def test_divide_query_string_and_parse(self):
        """
        Test method divide_query_string_and_parse
        """
        invalid_q1 = 'all.prep time: 222 AND fav.id: 111'
        invalid_q2 = 'fav.what: no OR fav.name: no'
        valid_q = 'all.cook time: 20 AND all.id: 111'
        self.assertEqual(-3, divide_query_string_and_parse(invalid_q1))
        self.assertEqual(-4, divide_query_string_and_parse(invalid_q2))
        self.assertEqual(('all', {'$and': [{'cook time': '20'}, {'id': '111'}]}),
                         divide_query_string_and_parse(valid_q))

    def test_check_content_type(self):
        """
        Test method check_content_type
        """
        field_yields = 'yields'
        field_name = 'name'
        cont_str = 'haha'
        cont_int = '2333'
        self.assertEqual(-5, check_content_type(field_yields, cont_str))
        self.assertEqual(1, check_content_type(field_yields, cont_int))
        self.assertEqual(0, check_content_type(field_name, cont_str))
        self.assertEqual(0, check_content_type(field_name, cont_int))


if __name__ == '__main__':
    unittest.main()
