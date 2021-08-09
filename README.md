<!--
title: 'AWS API for recognition of images'
layout: Doc
framework: v2
platform: AWS
language: python
authorLink: 'https://github.com/FlyOn21'
authorName: 'Zhohliev Pavlo'
-->

# AWS API for recognition of images

## Usage

### Deployment

This example is made to work with the Serverless Framework dashboard which includes advanced features like CI/CD,
monitoring, metrics, etc. 
##MacOS/Linux
 - Create yourself AWS account using the [link](https://portal.aws.amazon.com/billing/signup?redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation&language=ru_ru#/start). 
 - Use the [tutorial](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/) to create a user.
 - [Create s3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html) for uploud recognition images


To install the latest version serverless, run this command in your terminal:
```
curl -o- -L https://slss.io/install | bash
$ serverless login
```
Install the necessary plugins
```
$ serverless plugin install --name serverless-dotenv-plugin 
$ serverless plugin install --name serverless-python-requirements 
```
In the project folder, rename the ```example.env``` file to ```.env```, after which we fill in the environment variables necessary for deployment
```
REGION_NAME=deploy_region
ACCESS_KEY=your_access_key
SECRET_KEY=your_secret_key
BUCKET=name_your_bucket_to_uploud_images
```
Launching the deployment api
```
$ serverless deploy
```
After running deploy, you should see output similar to:

```bash
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Creating Stack...
Serverless: Checking Stack create progress...
........
Serverless: Stack create finished...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service aws-python-rest-api.zip file to S3 (711.23 KB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
.................................
Serverless: Stack update finished...
Service Information
service: aws-python-rest-api
stage: dev
region: us-east-1
stack: aws-python-rest-api-dev
resources: 12
api keys:
  None
endpoints:
  ANY - https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
functions:
  api: aws-python-rest-api-dev-hello
layers:
  None
```

_Note_: In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).

### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
```

Which should result in response similar to the following (removed `input` content for brevity):

```json
{
  "message": "Go Serverless v2.0! Your function executed successfully!",
  "input": {
    
  }
}
```

# Description API

This api implements two endpoints

- POST .../blobs 
- GET .../blobs/{blob_id}

When use POST endpoint, the request body must contain a callback url where you expect the result of the service
Examples:
```bash
{"calback_url": "http://your_callback_url.com"}
```
Response API for POST request
```bash
{
  "blob_id": "b1bb07b8-04c6-4f3e-9574-3c1d633f7a8e",
  "callback_url": "http://your_callback_url.com",
  "upload_url": "https://blobs.s3.eu-central-1.amazonaws.com/b1bb07b8-04c6-4f3e-9574-3c1d633f7a8e"
}
```
>```"blob_id"```: id records in the DynamoDB database where the result of the work will be recorded images recognition
```"callback_url"```: url for callback when the result of image recognition is ready    
```"upload_url"```: the link where the client uploaded image for recognition. Put request type. The link is valid for half an hour.
> 
Response API for GET requests
```bash
{
  "blob_id": "b1bb07b8-04c6-4f3e-9574-3c1d633f7a8e",
  "labels": [
        {
            "label": "Plan",
            "confidence": 85.03274536132812,
            "parents": ["Plot"]
        }, ...
        ]
}
```
> ```"blob_id"```: id of the requested entry in the database  
>```"labels"```: image recognition results

### API architecture
![API architecture](https://test-task-image-perfsys.s3.eu-central-1.amazonaws.com/Untitled+Diagram.png)