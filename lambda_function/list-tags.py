import json
import boto3
import base64
import uuid
import os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    if event['httpMethod'] == 'GET':
        table = dynamodb.Table('ass2-image-database')
        
        response = table.scan()
        data = response['Items']
        
        tags = set()
        while 'LastEvaluationKey' in response:
            response = table.scan(ExclusiveStartKey = response['LastEvaluationKey'])
            data.extend(response['Items'])
            
        for row in data:
            if row['tags'] is not None:
                for tag in row['tags']:
                    tags.add(tag)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'tags': list(tags)}), 'headers': {'Access-Control-Allow-Origin': '*'}
    }
