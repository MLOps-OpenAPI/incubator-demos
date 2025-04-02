#!/usr/bin/env python3

import boto3
import os
import json

from dotenv import load_dotenv

load_dotenv()

def initialize_s3_client() -> boto3.client:
    endpoint_url="https://minio-api-minio.apps.cluster-4ghn9.4ghn9.sandbox2431.opentlc.com"
    aws_access_key_id = os.environ.get("ACCESS_KEY")
    aws_secret_access_key = os.environ.get("SECRET_KEY")
    
    s3_client = boto3.client(
    service_name="s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    endpoint_url=endpoint_url,
    )
    return s3_client

def get_object(key: str, bucket: str, s3_client: boto3.client) -> dict:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)

def push_object(key: str, bucket: str, object: dict, s3_client: boto3.client):
    response = s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(object, indent=2)
    )
    print(response)

def main():
    #inference_route = os.environ.get("INFERENCE_ROUTE")
    s3_client = initialize_s3_client()
    #data_card = get_object(os.environ.get("DATA_CARD"), "data-cards", s3_client)
    model_request = get_object(os.environ.get("MODEL_REQUEST"), "request-models", s3_client)
    model_location, metadata = os.environ.get("MODEL_LOCATION"), json.loads(os.environ.get("METADATA"))
    model_request["model_location"] = model_location
    model_card = dict()
    model_card["model_request"] = os.environ.get("MODEL_REQUEST")
    model_card["data_cards"] = [os.environ.get("DATA_CARD")]
    model_card["metadata"] = metadata
    model_card["deployed_locations"] = [{
        "model_pull_location": model_location
    }]
    print(json.dumps(model_card, indent=2))
    print(json.dumps(model_request, indent=2))

    push_object(key=os.environ.get("MODEL_CARD_NAME"), bucket="model-cards", object=model_card, s3_client=s3_client)
    push_object(key=os.environ.get("MODEL_REQUEST"), bucket="request-models", object=model_request, s3_client=s3_client)

if __name__ == "__main__":
    main()
