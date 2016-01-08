import json
import requests
import os
from datetime import datetime
from datetime import timedelta
from decimal import *
from django.utils import timezone

import datetime
import time


# for password hashing
import uuid
import hashlib


def currency_converter(curr_from, curr_to, value_input):

    basepath = os.path.dirname(__file__)
    now = timezone.now()  # + timedelta(hours=3)
    file_name = "{}.json".format(now.strftime('%Y_%m_%d'))
    rel_filepath = os.path.join(basepath, "..", "tmp", file_name)
    abs_filepath = os.path.abspath(rel_filepath)

    # if file exist so we already have current currencies
    if os.path.isfile(abs_filepath):
        with open(abs_filepath, "r") as f:
            exchange = json.loads(f.read())
    else:
        response = requests.get('http://api.fixer.io/latest')
        exchange = json.loads(response.content.decode())
        with open(abs_filepath, "w") as f:
            f.write(response.content.decode())

    rates = exchange['rates']
    from_value = Decimal(rates.get(curr_from, '1'))
    to_value = Decimal(rates.get(curr_to, '1'))
    result = Decimal(value_input/from_value*to_value)
    return "{0:.2f}".format(result)


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    password = hashlib.sha256(salt.encode() + password.encode())
    return password.hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(
        salt.encode() + user_password.encode()
    ).hexdigest()


def take_date(srting_repr, timestamp=0):

    if timestamp:
        now = timestamp  # + timedelta(hours=3)
    else:
        now = timezone.now()  # + timedelta(hours=3)

    calc_functions = {
        'today': now - timedelta(hours=24),
        'week': now - timedelta(days=7),
        'month': now - timedelta(days=32),
        'year': now - timedelta(days=365),
        'beginning': now - timedelta(days=1000)
    }
    return calc_functions.get(srting_repr, now)


def seconds_from_last_moday(date_time):
    date = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    now = time.mktime(date.timetuple())
    last_monday = time.mktime(
        (date - datetime.timedelta(days=date.weekday())).timetuple())

    return now-last_monday


def ai_select_category(money, timedelta, user_id, payments_train_data):
    categories_data = tuple()
    print(money, timedelta, user_id, payments_train_data)
    # k = int(sys.argv[1:][0])
    # train_data = TrainData('iris_train.txt')
    # good_test = 0
    # with open('iris_test.txt') as test_file:
    #     test_data = test_file.readlines()
    #     with open('iris_test_result.txt') as test_result_file:
    #         result_data = test_result_file.readlines()
    #         index = 0
    #         for data in test_data:
    #             item = Item(data)
    #             classifier = Classifier(train_data, item)
    #             result = classifier.execute(k)
    #             if result != result_data[index].replace("\n", ""):
    #                 pass
    #             else:
    #                 good_test += 1
    #             index += 1

    #         print('Tests: {}% success!'.format(
    #             int((good_test/len(test_data))*100))
    #         )

    # if len(sys.argv[2:]):
    #     item = Item(sys.argv[2:][0])
    #     classifier = Classifier(train_data, item)
    #     result = classifier.execute(k)
    #     print('Class of item: ', result)

    return categories_data