import boto3
import os
import json
from typing import Tuple
import hashlib


from dotenv import load_dotenv

load_dotenv()

def update_model_card(data_card: dict):

    bucket_name = os.environ.get("BUCKET_NAME")
    endpoint_url=os.environ.get("S3_ENDPOINT")
    aws_access_key_id = os.environ.get("ACCESS_KEY")
    aws_secret_access_key = os.environ.get("SECRET_KEY")
    object_key = os.environ.get("FILE_NAME")

    s3_client = boto3.client(
        service_name="s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
    )

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(data_card, indent=2)
    )


def main():
    print(os.getcwd())
    model_card = json.loads(os.environ.get("MODEL_CARD"))
    model_location = os.environ.get("MODEL_PULL_LOCATION")

    model_card["model_pull_location"] = model_location
    print(json.dumps(model_card, indent=2))
    update_model_card(model_card)

if __name__ == "__main__":
    main()