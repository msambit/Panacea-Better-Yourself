import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource(service_name='dynamodb', region_name="us-east-1")
table = dynamodb.Table('mhcc_history')

client = boto3.client('cognito-idp')

# Context Handler
def lambda_handler(event, context):
    
    headers = event['headers']
    headerToken = headers.get('authToken')
    print(headerToken)
    
    response_cognito = client.get_user(AccessToken=headerToken)
    print(response_cognito)
    username = response_cognito['Username']
    print(username)
    
    items = table.get_item(Key={"id": username})
    print(items)
    
    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': { 
            "Access-Control-Allow-Origin": "*" 
        }
    }
