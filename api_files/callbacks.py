import requests

callback_headers = {"Content-Type": "application/json"}


def db_record_updated(event, _):
    print(event)

    for record in event.get("Records"):
        if record.get("eventName") != "MODIFY":
            continue

        blob = record.get("dynamodb").get("NewImage")

        labels_record = blob.get("labels")

        if not labels_record:
            continue

        labels = labels_record.get("S")
        callback_url = blob.get("callback_url").get("S")

        requests.post(url=callback_url, data=labels, headers=callback_headers)
