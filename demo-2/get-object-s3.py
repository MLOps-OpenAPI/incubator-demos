import boto3
import os
from io import BytesIO
import json
import botocore.exceptions
from dotenv import load_dotenv

load_dotenv()


def main():

    bucket_name = os.environ.get("BUCKET_NAME")
    endpoint_url=os.environ.get("S3_ENDPOINT")
    aws_access_key_id = os.environ.get("ACCESS_KEY")
    aws_secret_access_key = os.environ.get("SECRET_KEY")
    file_name = os.environ.get("FILE_NAME")

    s3_client = boto3.client(
        service_name="s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
    )

    try:
        # Download the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        content = response['Body'].read().decode('utf-8')

        # Try to parse the content as JSON
        try:
            json_object = json.loads(content)
            # Pretty print the JSON object
            print(json.dumps(json_object, indent=2))
        except json.JSONDecodeError:
            print("Error: The object is not valid JSON.")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Error: The object does not exist.")
        else:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()


