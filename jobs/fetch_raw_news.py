import sys
import requests
from datetime import date, timedelta, datetime
import boto3
import json

sns = boto3.client('sns')


def lambda_handler(event, context):
    API_KEY = "4cefc9e6993143918d8ef16329c3febb"
    try:
        page = 1
        articles = []
        current_date = date.today() - timedelta(days=1)
        while True:
            url = f'https://newsapi.org/v2/top-headlines?' \
                  f'from={current_date}&' \
                  f'sortBy=popularity&' \
                  f'language=en&' \
                  f'page={page}&' \
                  f'apiKey={API_KEY}'
            print(url)
            response = requests.get(url)

            raw_json = response.json()
            if raw_json.get('status') == 'ok':
                # pass raw_json.get('articles') to sns
                print(raw_json.get('articles'))
                if len(raw_json.get('articles')) == 0:
                    break
                else:
                    articles.extend(raw_json.get('articles'))
            else:
                break
            page = page + 1
        sns_body = {
            'articles': articles
        }
        sns_message = json.dumps(sns_body)
        sns = boto3.client('sns')
        response = sns.publish(TopicArn='arn:aws:sns:ap-south-1:402583888489:happy_news__raw_news_topic',
                               Message=sns_message,
                               Subject='Raw News')
        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'message': sns_message
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello')
    # }