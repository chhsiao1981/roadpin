# -*- coding: utf-8 -*-

import random
import math
import base64
import time
import ujson as json

from app import cfg
from app import util

def g_json_handler(start_timestamp, end_timestamp):
    start_timestamp = int(start_timestamp)
    end_timestamp = int(end_timestamp)

    cfg.logger.debug('start_timestamp: %s end_timestamp: %s', start_timestamp, end_timestamp)

    result_all = util.db_find('roadDB')
    #cfg.logger.debug('result_all: %s', result_all)

    results = [result for result in result_all if _is_valid(result, start_timestamp, end_timestamp)]

    return results


def _is_valid(result, start_timestamp, end_timestamp):
    if result['beginAt'] < start_timestamp and result['endAt'] < start_timestamp:
        return False

    if result['beginAt'] > end_timestamp and result['endAt'] > end_timestamp:
        return False

    return True
        
    
    
def _result_to_dict(result):
    return {str(val['beginAt']) + '_' + str(val['endAt']): val for val in result}
