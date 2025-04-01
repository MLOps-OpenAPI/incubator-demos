from flask import Flask, request, jsonify
import os
import boto3
import json
import botocore

app = Flask(__name__)

def get_object(file_type: str):
    request_body = request.data.decode("utf-8")
    if request_body:
        request_json = json.loads(request_body)
        try:

            bucket_name = request_json["Bucket"]
            aws_access_key_id = request_json["AccessKey"]
            aws_secret_access_key = request_json["SecretKey"]
            endpoint_url = request_json["S3Url"]
            
            #this allows us to grab a specific filetype
            file_name = request_json[file_type]
            
            s3_client = boto3.client(
            service_name="s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url,
            )
            # Download the object from S3
            response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
            content = response['Body'].read().decode('utf-8')

            # Try to parse the content as JSON
            try:
                json_object = json.loads(content)
                # Pretty print the JSON object
                json_output = json.dumps(json_object, indent=2)
                return content
            except json.JSONDecodeError:
                print("Error: The object is not valid JSON.")

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("Error: The object does not exist.")
            elif e.response['Error']['Code'] == 'NoSuchKey':
                print("Error: The key does not exist")
            else:
                print(f"Error: {e}")
            
    else:
        return jsonify(request_body)


@app.route('/get-data-card', methods=["GET"])
def get_data_card():
    return get_object("DataCard")

@app.route('/get-model-card', methods=["GET"])
def get_model_card():
    return get_object("ModelCard")

@app.route('/get-model-card-request', methods=["GET"])
def get_model_card_request():
    return get_object("ModelCardRequest")


if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')