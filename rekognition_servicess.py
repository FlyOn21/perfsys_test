import json
import os
import boto3

dynamodb_client = boto3.client("dynamodb")
BLOBS_TABLE = os.environ["BLOBS_TABLE"]


def _process_blob(uuid):
    client = boto3.client("rekognition", region_name= os.environ["REGION_NAME"],
                            aws_access_key_id=os.environ["ACCESS_KEY"],
                            aws_secret_access_key=os.environ["SECRET_KEY"]
                          )
    response = client.detect_labels(
        Image={
            "S3Object": {
                "Bucket": os.environ["BUCKET"],
                'Name': uuid
            }
        },
        MaxLabels=200,
        MinConfidence=20
    )
    return response


def uploaded_file(event, _):
    blob_id = event["Records"][0]["s3"]["object"]["key"]
    recognition_result = _process_blob(uuid=blob_id)
    _update_db_unit(blob_id=blob_id, labels=recognition_result.get("Labels"))


def _update_db_unit(labels, blob_id):
    projections = []
    for label in labels:
        parents = []
        for parent in label.get("Parents"):
            parents.append(parent.get("Name"))

        projections.append({
            "label": label.get("Name"),
            "confidence": label.get("Confidence"),
            "parents": parents
        })

    projections_data = json.dumps(projections)

    dynamodb_client.update_item(
        TableName=BLOBS_TABLE,
        Key={
            "id": {"S": blob_id}
        },
        UpdateExpression="set labels=:value",
        ExpressionAttributeValues={
            ":value": {"S": projections_data}
        }
    )
    return projections_data
