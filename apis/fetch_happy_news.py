import simplejson as json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('happy_news__news_table')
    response = table.query(KeyConditionExpression=Key('ID').eq('POSITIVE'), ScanIndexForward=False, Limit=2)
    response['event']=event["queryStringParameters"]
    print(response)
    # TODO implement
    return {
        "isBase64Encoded": True,
        "statusCode": 200,
        "headers": { "headerName": "headerValue"},
        "body": json.dumps(response)
    }
