import boto3
import botocore
import os
from io import BytesIO
import json
import botocore.exceptions
from dotenv import load_dotenv

load_dotenv()


def main():

    BUCKET_NAME = "data-cards"

    aws_access_key_id = os.environ.get("ACCESS_KEY")
    aws_secret_access_key = os.environ.get("SECRET_KEY")

    s3_client = boto3.client(
        service_name="s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        # TODO: Change hard-coded endpoint
        endpoint_url="https://minio-api-minio.apps.cluster-497z4.497z4.sandbox2736.opentlc.com",
    )

    event = dict()
    event["eventName"] = os.environ.get("EVENT_NAME")
    event["key"] = os.environ.get("KEY")
    event["records"] = json.loads(os.environ.get("RECORDS"))
    event["endpoint"] = os.environ.get("ENDPOINT")

    try:
        # Check if the object already exists
        s3_client.head_object(Bucket=BUCKET_NAME, Key=event["key"])
        print(f"File {event['key']} already exists in the bucket.")

        # Read the contents of the existing file in S3
        existing_file = s3_client.get_object(Bucket=BUCKET_NAME, Key=event["key"])
        existing_file_content = existing_file["Body"].read().decode("utf-8")
        existing_file_json = json.loads(existing_file_content)

        # Append to Records list if data card already exists for the bucket
        for event_record in existing_file_json["records"]:
            event["records"].append(event_record)

        json_event = json.dumps(event)
        bytes_data = bytes(str(json_event), "utf-8")
        # Create a file object
        file_obj = BytesIO(bytes_data)

        # Upload the combined content to S3
        s3_client.put_object(Body=file_obj, Bucket=BUCKET_NAME, Key=event["key"])
        print(f"Combined file uploaded to {event['key']} in S3.")

    except botocore.exceptions.ClientError as e:
        print("exception caught", e.response["Error"]["Code"])
        # If the object doesn"t exist, upload the new file
        if e.response["Error"]["Code"] == "404":

            json_event = json.dumps(event)
            bytes_data = bytes(str(json_event), "utf-8")
            # Create a file object
            file_obj = BytesIO(bytes_data)

            s3_client.put_object(Body=file_obj, Bucket=BUCKET_NAME, Key=event["key"])
            print(f"Bucket {BUCKET_NAME} created.")
            print(f"File {event['key']} uploaded to S3.")

        else:
            # Reraise other types of errors
            raise


if __name__ == "__main__":
    main()
