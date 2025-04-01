#!/usr/bin/env python3

import boto3
import os
import json

from dotenv import load_dotenv

load_dotenv()

def initialize_s3_client() -> boto3.client:
    endpoint_url=os.environ.get("S3_ENDPOINT")
    aws_access_key_id = os.environ.get("ACCESS_KEY")
    aws_secret_access_key = os.environ.get("SECRET_KEY")
    
    s3_client = boto3.client(
    service_name="s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    endpoint_url=endpoint_url,
    )
    return s3_client

def get_model_card(s3_client: boto3.client) -> dict:
    bucket_name = os.environ.get("BUCKET_NAME")
    file_name = os.environ.get("FILE_NAME")
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)

def update_model_card(data_card: dict, s3_client: boto3.client):
    bucket_name = os.environ.get("BUCKET_NAME")
    object_key = os.environ.get("FILE_NAME")

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json.dumps(data_card, indent=2)
    )
    print(response)

def main():
    print(os.getcwd())
    inference_route = os.environ.get("INFERENCE_ROUTE")
    s3_client = initialize_s3_client()
    model_card = get_model_card(s3_client)
    #model_location = os.environ.get("MODEL_PULL_LOCATION")

    if "deployed_locations" not in model_card:
        model_card["deployed_locations"] = [inference_route]
    else:
        if inference_route not in model_card["deployed_locations"]:
            model_card["deployed_locations"].append(inference_route)
        else:
            print(f"deploy location: {inference_route} is already in model card {os.environ.get("FILE_NAME")}")
    print(model_card)
    print(json.dumps(model_card, indent=2))
    update_model_card(model_card, s3_client)

if __name__ == "__main__":
    main()
