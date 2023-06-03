import json
import boto3
import logging
import os
import uuid
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    # TODO implement
    logger.info(event)
    logger.info(os.environ)
    message = event['Records'][0]['Sns']['Message']
    news = json.loads(message)

    sid_obj = SentimentIntensityAnalyzer()

    positive_articles = []
    for article in news['articles']:
        sentence = article['title'] + ' | ' + article['content'] + ' | ' + article['description']
        sentiment_dict = sid_obj.polarity_scores(sentence)
        article['sentiment'] = 'POSITIVE' if sentiment_dict['compound'] >= 0.05 else 'NEGATIVE'
        # if article['sentiment'] == 'POSITIVE':
        article['ID'] = article['sentiment']
        article['epoch_in_milliseconds'] = round(time.time() * 1000)
        write_to_db(article)

    return {
        'statusCode': 200,
        'body': event
    }


def write_to_db(data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('happy_news__news_table')

    table.put_item(
        Item=data
    )