import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import object_detection
import base64

# Bucket and Dynamodb
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # TODO implement

    if event['httpMethod'] == "POST":
        # get JSON object from POST request
        data = json.loads(event['body'])
        
        # image should be in base64 string encoding already
        imageData = data['image']
        tags = object_detection.detect_image(imageData)
        
        # connect to dynamoDB table
        table = dynamodb.Table('ass2-image-database')
        
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
            
        # # Put into required json format
        response = {"links": links}
        
        # JSON reponse of successful POST
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {'Access-Control-Allow-Origin': '*'}
        }