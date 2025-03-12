import boto3
import botocore
import os
from io import BytesIO
import json
import time
import botocore.exceptions
from dotenv import load_dotenv

load_dotenv()

def main():

    aws_access_key_id = os.environ.get('ACCESS_KEY')
    aws_secret_access_key = os.environ.get('SECRET_KEY')

    s3_client = boto3.client(
        service_name='s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url="https://minio-api-minio.apps.cluster-497z4.497z4.sandbox2736.opentlc.com"
    )

    # with open("create_event.json", "r") as file:
    #     data = json.load(file)

    data = json.loads(os.environ.get('payload_body'))

    object_key = data['Records'][0]['s3']['object']['key']

    
    current_time = str(time.time())

    bucket_name = "data-cards"
    #destination_file = "my-test-file2.txt"
    object_key = object_key + current_time + ".json"
    bytes_data = bytes(str(data), "utf-8")
        # Create a file object
    file_obj = BytesIO(bytes_data)   
    try:
        # Check if the object already exists
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        print(f"File {object_key} already exists in the bucket.")
        
        # Read the contents of the existing file in S3
        existing_file = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        existing_file_content = existing_file['Body'].read().decode('utf-8')

        # Combine both files
        combined_content = existing_file_content + '\n' + str(data)
        
        # Upload the combined content to S3
        s3_client.put_object(Body=combined_content, Bucket=bucket_name, Key=object_key)
        print(f"Combined file uploaded to {object_key} in S3.")
    
    except botocore.exceptions.ClientError as e:
        print("exception caught", e.response['Error']['Code'])
        # If the object doesn't exist, upload the new file
        if e.response['Error']['Code'] == 'NoSuchKey':
            s3_client.put_object(Body=data, Bucket=bucket_name, Key=object_key)
            print(f"File {object_key} uploaded to S3.")
        elif e.response['Error']['Code'] == "404":
            s3_client.put_object(Body=file_obj, Bucket=bucket_name, Key=object_key)
            print(f"Bucket {bucket_name} created.")
            print(f"File {object_key} uploaded to S3.")

        else:
            # Reraise other types of errors
            raise
    

if __name__ == "__main__":
    main()