from unittest import TestCase
from utils.pagination import make_pagination_range

class PaginationFuncTest(TestCase):

    def test_if_initial_ranges_are_correct(self):

        self.assertEqual([1,2,3,4],make_pagination_range()['pagination'])

        self.assertEqual([1,2,3,4],make_pagination_range(current_page=2)['pagination'])

    def test_if_middle_ranges_are_correct(self):
        
        self.assertEqual([8,9,10,11],make_pagination_range(current_page=9)['pagination'])

        self.assertEqual([14,15,16,17],make_pagination_range(current_page=15)['pagination'])

    def test_final_range_is_correct(self):
        self.assertEqual([17,18,19,20],make_pagination_range(current_page=18)['pagination'])

        self.assertEqual([17,18,19,20],make_pagination_range(current_page=19)['pagination'])

        self.assertEqual([17,18,19,20],make_pagination_range(current_page=20)['pagination'])

        self.assertEqual([17,18,19,20],make_pagination_range(current_page=21)['pagination'])