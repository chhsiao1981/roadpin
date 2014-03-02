# -*- coding: utf-8 -*-

import logging
import unittest
from app.crawlers.taipei_city import crawler_taipei_city_road_case

class TestCrawlerTaipeiCityRoadCase(unittest.TestCase):
    '''unit tests for crawler_taipei_city_road_case'''

    def setUp(self):
        '''setup for all the tests'''
        logging.info('setup')
        self.____never_used_variable = 1

    def tearDown(self):
        '''teardown for all the tests'''
        logging.info("teardown")

    def test_crawler_taipei_city_road_case_true(self):
        '''True should not assert.'''
        assert True

    def test_bottle_tmp_never_used_variable_as_1(self):
        '''a == 1 should not assert.'''
        logging.info("test_bottle_tmp: test_bottle_tmp_true")
        assert self.____never_used_variable == 1
