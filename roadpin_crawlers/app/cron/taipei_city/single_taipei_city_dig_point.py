# -*- coding: utf-8 -*-

from app.constants import S_OK, S_ERR
import random
import math
import base64
import time
import ujson as json
import argparse

from app import cfg
from app import util
from app import crawlers
from app.crawlers.taipei_city import crawler_taipei_city_dig_point
from app.cron.taipei_city import cron_taipei_city_dig_point

def single_taipei_city_dig_point(filename):
    dig_points = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        dig_points = [int(line) for line in lines]

    (error_code, http_results) = crawler_taipei_city_dig_point._get_http_results(dig_points)
    #cfg.logger.debug('after _get_http_results: error_code: %s', error_code)
    if error_code != S_OK:
        cfg.logger.error('unable to get http_result: dig_points: %s', dig_points)
        return error_code

    (error_code, next_dig_point, data) = crawler_taipei_city_dig_point._process_http_results(dig_points, http_results)
    #cfg.logger.debug('after _process_http_results: error_code: %s, next_dig_point: %s results: %s', error_code, next_dig_point, results)
    if error_code != S_OK:
        return error_code

    data = data.values()
    crawlers.set_county_name(data, '臺北市')
    crawlers.set_category(data, 'taipei_city_dig_point')

    results = {"data": data}

    cron_taipei_city_dig_point._process_results(results)

    return S_OK


def parse_args():
    ''' '''
    parser = argparse.ArgumentParser(description='roadpin_backend')
    parser.add_argument('-i', '--ini', type=str, required=True, help="ini filename")
    parser.add_argument('-f', '--filename', type=str, required=True, help="idx")

    args = parser.parse_args()

    return (S_OK, args)


if __name__ == '__main__':
    (error_code, args) = parse_args()

    cfg.init({"ini_filename": args.ini})

    single_taipei_city_dig_point(args.filename)
