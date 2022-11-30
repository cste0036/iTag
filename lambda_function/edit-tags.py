import json
import boto3

# Dynamo Database
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    
    # API is reached through POST
    if event['httpMethod'] == "POST":
        
        # Extract the data from the POST JSON data
        table = dynamodb.Table('ass2-image-database')
        data = json.loads(event['body'])
        
        # Store the s3-url and the Tag Information
        s3_url = data['s3_url']
        type_flag = data['type']
        user_tags = data['tags']
        
        # Type_flag == 1 - ADD TAGS
        if(type_flag == '1'):
            
            try:
                # Read the curently recorded tags of the image in the DB
                item = table.get_item(Key={'s3-url': s3_url})
                item_tags = item["Item"]["tags"]
                
                # If the user submitted tag is new, add it to the list
                for tag in user_tags:
                    if tag not in item_tags:
                        item_tags.append(tag)
                
                # Attempt to update the tags for the specified image
                try:
                    table.put_item(Item={'s3-url': s3_url,'tags': item_tags})
                    response = s3_url + " Tags Added!"
                except:
                    print("Tags could not be added")
                    response = s3_url + " Tags could not be added..."
                
            except Exception:
                print("Item associated to url could not be found.")
                
            
        # Type_flag == 0 - REMOVE TAGS
        elif (type_flag == '0'):
            
            try:
                # Read the curently recorded tags of the image in the DB
                item = table.get_item(Key={'s3-url': s3_url})
                item_tags = item["Item"]["tags"]
                print("Item tags:")
                print(item_tags)
                
                # If the user submitted tag is new, add it to the list
                for tag in user_tags:
                    if tag in item_tags:
                        item_tags.remove(tag)
                
                # Attempt to update the tags for the specified image
                try:
                    table.put_item(Item={'s3-url': s3_url,'tags': item_tags})
                    response = s3_url + " Tags Deleted!"
                except:
                    print("Tags could not be deleted")
                    response = s3_url + " Tags could not be deleted..."
                    

            except Exception:
                print("Item associated to url could not be found.")
                
        
        #response = s3_url + " Updated"

        return {
            "statusCode": 200,
            "body": json.dumps(response),
            'headers': {'Access-Control-Allow-Origin': '*'}
        }
        
    
# Test Data    
"""
    {
    "s3-url":"s3://ass2-images/images/test12",
    "type":"1",
    "tags":[ "test", "person", "car" ]
    }
"""