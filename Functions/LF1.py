import json
import logging
import boto3
import os
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ENDPOINT = os.environ['ENDPOINT_NAME']
print(ENDPOINT)
runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='us-east-1')

dynamodb = boto3.resource(service_name='dynamodb', region_name="us-east-1")
table = dynamodb.Table('mhcc_history')

client = boto3.client('cognito-idp')

# Context Handler
def lambda_handler(event, context):
    
    requestBody  = json.loads(event['body'])
    message = requestBody["messages"]
    print(message)
    
    headers = event['headers']
    headerToken = headers.get('authToken')
    print(headerToken)
    
    parameters = {'return_all_scores':True}
    payload = json.dumps({'inputs': message, 'parameters': parameters})
    print(payload)
    
    sagemaker_result = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='application/json', Body=payload)
    response = json.loads(sagemaker_result["Body"].read().decode("utf-8"))
    print(response)

    #get current date
    dt = datetime.today()  
    seconds = int(dt.timestamp())
    print(seconds)
    
    response_cognito = client.get_user(AccessToken=headerToken)
    print(response_cognito)
    username = response_cognito['Username']
    print(username)
    
    result = table.update_item(
    Key={
        'id': username
    },
    UpdateExpression="SET times = list_append(if_not_exists(times, :empty_list), :myvalue1), labels = list_append(if_not_exists(labels, :empty_list), :myvalue2)",
    ExpressionAttributeValues={
        ':myvalue1': [str(seconds)],
        ':myvalue2': [str(response[0])],
        ":empty_list": []
    },
    ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response[0]),
        'headers': { 
            "Access-Control-Allow-Origin": "*" 
        }
    }