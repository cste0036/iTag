import json
import base64
import boto3
s3 = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    
    if event['httpMethod'] == "POST":
        #get the data from post
        data = json.loads(event['body'])
        name = data['name']
        #let image go to image file
        name = "images/" + name
        image = data['file']
        #decode image
        image = base64.b64decode(image)

    # s3.generate_presigned_url(
    #     ClientMethod='put_object', 
    #     Params={'Bucket': 'ass2-images','Key': name},
    #     ExpiresIn=3600)
        
        
        
        
 ## modified from 
# https://github.com/williamtnguyen/SJSU-TT/blob/474a01811c91123f3623abe7f3a0d0d7c5913671/server/routes/api/services/upload-s3.js   
    s3.put_object(
         Bucket ='ass2-images',
         Key = name,
         Body = image,
         ContentType = 'mimetype',
         ContentDisposition = 'inline',
         ACL = 'public-read'
         )

    return {
        'statusCode': 200,
        'body': json.dumps({"res": "test"}),
        'headers': {'Access-Control-Allow-Origin': '*'}
    }