import sys
import requests
from datetime import date, timedelta, datetime

import json


def lambda_handler(event, context):
    API_KEY = "4cefc9e6993143918d8ef16329c3febb"
    try:
        current_date = date.today() - timedelta(days=1)
        url = f'https://newsapi.org/v2/top-headlines?' \
              f'from={current_date}&' \
              f'sortBy=popularity&' \
              f'language=en&' \
              f'page={datetime.now().hour + 1}&' \
              f'apiKey={API_KEY}'
        print(url)
        response = requests.get(url)

        raw_json = response.json()
        if raw_json.get('status') == 'ok':
            # pass raw_json.get('articles') to kinesis
            print(raw_json.get('articles'))
    except Exception as e:
        print(e)
