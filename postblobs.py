import json
import os
import uuid

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

dynamodb_client = boto3.client("dynamodb")
BLOBS_TABLE = os.environ["BLOBS_TABLE"]

response_bad_request = {"statusCode": 400, "body": json.dumps({"error": "Invalid callback url supplied"})}


def _upload_url(uuid):
    clients = boto3.client("s3", config=Config(signature_version="s3v4"),
                           region_name=os.environ["REGION_NAME"],
                           aws_access_key_id=os.environ["ACCESS_KEY"],
                           aws_secret_access_key=os.environ["SECRET_KEY"])
    try:
        url = clients.generate_presigned_url(
            ClientMethod="put_object",
            Params={"Bucket": os.environ["BUCKET"], "Key": uuid},
            ExpiresIn=1800)

        return url
    except ClientError as e:
        return e


def create_blob(event, context):
    event_body = event.get("body")
    if not event_body:
        return response_bad_request

    request_body = json.loads(event_body)

    callback_url = request_body.get("callback_url")
    if not callback_url:
        return response_bad_request

    blob_id = str(uuid.uuid4())

    dynamodb_client.put_item(
        TableName=BLOBS_TABLE, Item={"id": {"S": blob_id}, "callback_url": {"S": callback_url}}
    )
    upload_url_create = _upload_url(uuid=blob_id)

    body = {
        "blob_id": blob_id,
        "callback_url": callback_url,
        "upload_url": upload_url_create
    }

    return {
        "statusCode": 201,
        "body": json.dumps(body)
    }
