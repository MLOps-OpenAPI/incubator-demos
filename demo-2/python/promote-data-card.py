import boto3
import os
import json
from typing import Tuple
import hashlib


from dotenv import load_dotenv

load_dotenv()

def set_hash(data_card: dict):
    buckets_string = str(data_card["buckets"])
    print(f"Bucket info that is being hashed:\n{buckets_string}\n")
    data_card["hash"] = hashlib.sha256(str.encode(buckets_string)).hexdigest()


def check_hash(data_card: dict) -> Tuple[bool, str]:
    buckets_string = str(data_card["buckets"])
    print(f"Bucket info that is being hashed:\n{buckets_string}\n")
    data_card_hash = hashlib.sha256(str.encode(buckets_string)).hexdigest()

    return data_card["hash"] == data_card_hash, data_card_hash

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
    print(os.getcwd())
    # with open("incubator-demos/demo-2/python/promote-data-card.py", "r") as f:
    #     data_card = json.load(f)
    data_card = json.loads(os.environ.get("DATA_CARD"))

    #setting the hash
    set_hash(data_card)

    #checking the hash
    matches, desired_hash = check_hash(data_card)

    if matches:
        data_card["golden"] = True
        print(json.dumps(data_card, indent=2))
        update_data_card(data_card)
    else:
        print("error, the hash does not match.  This could indicate tampering")
        print(f"current hash: {data_card['hash']}\nWhat the hash should be: {desired_hash}")



if __name__ == "__main__":
    main()