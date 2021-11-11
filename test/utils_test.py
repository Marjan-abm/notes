"""
Test module for utils
"""
import unittest

from scraper.utils import is_id_present, json_file_to_dict


class TestUtils(unittest.TestCase):
    """
    Test class for utils.py
    Method export_to_json_file will be tested in manual test plan.
    Methods update_by_json_file, insert_by_json_file are not tested because they mainly calls
    json_file_to_dict, update_on_tb, and insert_into_tb, which are already tested.
    """

    def test_is_id_present(self):
        """
        Test method is_id_present
        """
        no_id_dict = {'what?': 'no id!'}
        empty_dict = {'id': '', 'it is': 'not good'}
        letter_id_dict = {'id': 'qq', 'it is': 'not good'}
        valid_dict = {'id': '123', 'message': 'yes'}
        self.assertFalse(is_id_present(no_id_dict))
        self.assertFalse(is_id_present(empty_dict))
        self.assertFalse(is_id_present(letter_id_dict))
        self.assertTrue(is_id_present(valid_dict))

    def test_json_file_to_dict(self):
        """
        Test method json_file_to_dict
        """
        my_dict = {'id': '3512',
                   'name': 'Test Food',
                   'description': 'Just for test'}
        res_dict = json_file_to_dict('json_file_to_dict_test.json')
        self.assertEqual(my_dict, res_dict)


if __name__ == '__main__':
    unittest.main()
