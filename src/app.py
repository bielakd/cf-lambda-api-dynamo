import os
import uuid

from dynamo_db.context import SetupDynamoContext
from dynamo_db.builder import Container
from dynamo_db.dynamo_operations import InitDynamoDB, ExtractMessageDynamoDB
from dynamo_db.helpers import DecimalEncoder
from dynamo_db.processor import Processor


def handler(context, event):
    correlation_id = str(uuid.uuid4())
    print(f"--^^^{correlation_id}")
    dynamo_context = gen_context(correlation_id=correlation_id)
    container = build(context=dynamo_context)
    return Processor(container=container).run(message_key=correlation_id)


def build(context: SetupDynamoContext):
    container = Container(
        initiator=InitDynamoDB(context=context),
        extractor=ExtractMessageDynamoDB(context=context, decimal_encoder=DecimalEncoder),
    )
    return container


def gen_context(correlation_id: str) -> SetupDynamoContext:
    import boto3
    context = SetupDynamoContext(
        client=boto3.resource("dynamodb", region_name=os.getenv("REGION", KeyError)),
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
