import os
import uuid
import json
from dynamo_db.context import SetupDynamoContext
from dynamo_db.builder import Container
from dynamo_db.dynamo_operations import InitDynamoDB, ExtractMessageDynamoDB
from dynamo_db.processor import Processor


def handler(context, event):
    correlation_id = str(uuid.uuid4())
    dynamo_context = gen_context(correlation_id=correlation_id)
    container = build(context=dynamo_context)
    return Processor(container=container).run(message_key=correlation_id)



    # print("Starting Execution")
    # print(event)
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({"payload": "Hello World"}),
    #     "isBase64Encoded": False
    # }


def build(context: SetupDynamoContext):
    container = Container(
        initiator=InitDynamoDB(context=context),
        extractor=ExtractMessageDynamoDB(),
    )
    return container


def gen_context(correlation_id: str) -> SetupDynamoContext:
    import boto3
    context = SetupDynamoContext(
        client=boto3.client("dynamodb"),
        table_name=os.getenv("DYNAMO_TABLE", KeyError),
        pk="correlationId",
        data={
            "correlationId": correlation_id,
            "payload": {
                "message": "Hello World",
                "src": "dynamoDb"
            }
        }
    )
    return context
