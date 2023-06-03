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
              f'page={0 + 1}&' \
              f'apiKey={API_KEY}'
        print(url)
        response = requests.get(url)

        raw_json = response.json()
        if raw_json.get('status') == 'ok':
            # pass raw_json.get('articles') to sns
            print(raw_json.get('articles'))
            sns_body = {
                'articles': raw_json.get('articles')
            }
            sns_message = json.dumps(sns_body)
            # sns = boto3.client('sns')
            # response = sns.publish(TopicArn='arn:aws:sns:ap-south-1:402583888489:happy_news__raw_news_topic',
            #             Message=sns_message,
            #             Subject='Raw News')
            # return {
            #     'statusCode': 200,
            #     'body': json.dumps(response)
            # }
        else:
            print('Error fetching news')
            print(raw_json)
            return {
                'statusCode': 401,
                'body': json.dumps(raw_json)
            }
    except Exception as e:
        print(e)
        return {
                'statusCode': 500,
                'body': json.dumps(e)
            }

lambda_handler(None, None)