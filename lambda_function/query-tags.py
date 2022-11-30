import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Bucket and Dynamodb
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # TODO implement
    
    # API is reached through POST
    if event['httpMethod'] == "POST":
        
        # connect to the DynamoDB database
        table = dynamodb.Table('ass2-image-database') # 'ass2-image-database' for actual db, image for test
        # get JSON object from POST request
        data = json.loads(event['body'])
        
        # Store the s3-url and the Tag Information
        tags = data['tags']
        
        # list to store links of all matching items
        links = []
        
        # loop through the list of tags in json input
        for each in tags:
            try:
                # scan the dynamoDB for matching tags
                query = table.scan(
                    FilterExpression = Attr('tags').contains(each)
                    )
                
                # retrive s3 url from match and place into links list
                result = query['Items']
                
                for item in result:
                    links.append(item['s3-url'])
            except e:
                print(e)
        
        # Remove duplicate link entries
        links = list(set(links))
        
        # Put into required json format
        response = {"links": links}
        
        # JSON reponse of successful POST
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {'Access-Control-Allow-Origin': '*'}
        }
		
