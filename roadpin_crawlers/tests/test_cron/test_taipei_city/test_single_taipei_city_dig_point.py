# -*- coding: utf-8 -*-

import logging
import unittest
from app.cron.taipei_city import single_taipei_city_dig_point

class TestSingleTaipeiCityDigPoint(unittest.TestCase):
    '''unit tests for single_taipei_city_dig_point'''

    def setUp(self):
        '''setup for all the tests'''
        logging.info('setup')
        self.____never_used_variable = 1

    def tearDown(self):
        '''teardown for all the tests'''
        logging.info("teardown")

    def test_single_taipei_city_dig_point_true(self):
        '''True should not assert.'''
        assert True

    def test_bottle_tmp_never_used_variable_as_1(self):
        '''a == 1 should not assert.'''
        logging.info("test_bottle_tmp: test_bottle_tmp_true")
        assert self.____never_used_variable == 1