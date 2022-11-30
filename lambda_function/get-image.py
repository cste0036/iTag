import base64
import json
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    
    if event['httpMethod'] == "POST":
        
        #get the data from the request
        data = json.loads(event['body'])
        
        s3_url = data['s3_url']
        
        # Get the s3 bucket image key from the URL
        image_name = s3_url.split("/")
        image_key = image_name[3] + "/" + image_name[4]
        
        
        try:
            # Get the image from the s3 bucket
            image = s3.get_object(
                Bucket = 'ass2-images',
                Key = image_key
                )
            
            # Convert the retrieved image to Base64 encoded data
            imageData = base64.b64encode(image["Body"].read()).decode('utf-8')
            response_info = image_key + " Retrieved!"
        
        except:
            response_info = "Failed to find image."
            
        # Create the response JSON
        response = {"info": response_info, "image": imageData}

        return {
            "statusCode": 200,
            "body": json.dumps(response), 
            'headers': {'Access-Control-Allow-Origin': '*'}
        }