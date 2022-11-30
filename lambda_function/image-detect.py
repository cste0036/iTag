import json
import boto3
import object_detection
import base64

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    # TODO implement

    for record in event['Records']:
        # get bucket and key
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        image = s3_client.get_object(Bucket=bucket, Key=key)
        # encode the image
        imageData = base64.b64encode(image["Body"].read()).decode('utf-8')
        tags = object_detection.detect_image(imageData)
        s3_url = "https://ass2-images.s3.amazonaws.com/"+key

        table = dynamodb.Table('ass2-image-database')
        response = table.put_item(
            Item={
                's3-url': s3_url,
                'tags': tags

            })

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from detecting image!')
    }
