import boto3
import os
from io import BytesIO
import json
import botocore.exceptions
import ast

from dotenv import load_dotenv

load_dotenv()

def check_hash(data_card: dict) -> bool:

    #TODO: Implement hashing function

    return data_card["hash"] == "abcd1234"

def update_data_card(data_card: dict):

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
    print(response)


def main():
    print("hello_world")
    with open("/Users/akugel/Documents/Projects/global_stp_engagements/army/incubator-demos/demo-2/python/data_card_example.json", "r") as f:
        data_card = json.load(f)
    #data_card = json.loads(os.environ.get("DATA_CARD"))

    # Dummy hash for now
    data_card["hash"] = "abcd1234"
    
    if check_hash(data_card):
        data_card["golden"] = True

    print(json.dumps(data_card, indent=2))
    update_data_card(data_card)


if __name__ == "__main__":
    main()