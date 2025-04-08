import boto3
import os
import json

# from dotenv import load_dotenv

# load_dotenv()

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
    print(response)

def main():
    print(os.getcwd())
    #model_card = json.loads(os.environ.get("MODEL_CARD"))
    model_card = '''
    {
    "model_name": "granite-7b-instruct",
    "model_version": "1.0",
    "license": "Apache 2.0",
    "developer": "Granite AI Research",
    "description": "Granite-7B-Instruct is a 7-billion parameter instruction-tuned language model optimized for natural language understanding and generation tasks.",
    "architecture": "Transformer-based decoder model",
    "training_data": "Trained on a diverse mixture of open-domain datasets, including Common Crawl, Wikipedia, books, and high-quality instruction-tuning datasets.",
    "parameters": {
        "num_parameters": "7 billion",
        "hidden_size": 4096,
        "num_layers": 32,
        "num_attention_heads": 32
    },
    "capabilities": [
        "Text completion",
        "Question answering",
        "Summarization",
        "Code generation",
        "Conversational AI"
    ],
    "limitations": [
        "May generate incorrect or biased responses.",
        "Struggles with highly specialized or niche knowledge.",
        "Limited reasoning depth compared to larger models."
    ],
    "use_cases": [
        "Chatbots and virtual assistants",
        "Automated content generation",
        "Document summarization",
        "Educational tutoring"
    ],
    "source_data": {
        "data_cards": [
        ],
        "model_cards": [
        "huggingface.co/ibm-granite/granite-7b-instruct"
        ]
    },
    "deployment": {
        "frameworks": ["PyTorch", "Transformers (Hugging Face)", "ONNX Runtime", "vLLM"],
        "hardware_requirements": "Recommended: A100 (40GB) or higher GPU for inference."
    },
    "ethical_considerations": {
        "bias_mitigation": "Efforts have been made to reduce biases, but some biases may still be present.",
        "misuse_prevention": "Not intended for use in critical decision-making without human oversight."
    },
    "citation": "Granite AI Research, 'Granite-7B-Instruct: A Scalable Instruction-Tuned Language Model', 2025.",
    "model_pull_location": "https://minio-api-minio.apps.cluster-vtmgm.vtmgm.sandbox441.opentlc.com/model-bucket/granite-7b-instruct",
    "deployed_locations": [

    ]
    } '''
    model_card = json.loads(model_card)
    endpoint = model_card["model_pull_location"].split('/')[2]
    bucket = model_card["model_pull_location"].split('/')[3]
    directory = ''.join(model_card["model_pull_location"].split('/')[4:])

    print(model_card)
    print(endpoint + '\n' + bucket + '\n' + directory)

    # model_card["model_pull_location"] = model_location
    # print(json.dumps(model_card, indent=2))
    # update_model_card(model_card)

if __name__ == "__main__":
    main()