import json
import boto3

# Bucket and Dynamodb
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # TODO implement
    
    # API is reached through POST
    if event['httpMethod'] == "POST":
        
        # Extract the s3_url from the POST JSON data
        table = dynamodb.Table('ass2-image-database')
        data = json.loads(event['body'])
        s3_url = data['s3_url']
        
        # Get the s3 bucket image key from the URL
        image_name = s3_url.split("/")
        image_key = image_name[3] + "/" + image_name[4]
        
        try:
            # Delete the image from the s3 bucket
            s3.delete_object(
                Bucket = 'ass2-images',
                Key = image_key
                )
            
            # Delete the image tag data from the Dynamo Database
            table.delete_item(
                Key={
                's3-url': s3_url
                })
        except:
            print("Error")
            response_info = s3_url + " NOT FOUND"
        
        response_info = s3_url + " DELETED"
        response = {"info": response_info}

        return {
            "statusCode": 200,
            "body": json.dumps(response), 
            'headers': {'Access-Control-Allow-Origin': '*'}
        }