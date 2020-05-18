import os
from unittest import mock

import boto3
import pytest
from moto import mock_dynamodb2_deprecated, mock_dynamodb2

from dynamo_db.context import SetupDynamoContext
from dynamo_db.dynamo_operations import InitDynamoDB, ExtractMessageDynamoDB
from dynamo_db.helpers import DecimalEncoder


@mock_dynamodb2
@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("REGION", "us-east-1")
    db = boto3.resource("dynamodb", region_name=os.getenv("REGION", KeyError))

    return db


@pytest.fixture
def context(monkeypatch, client):
    monkeypatch.setenv("DYNAMO_TABLE", "TestTable")
    context = SetupDynamoContext(
        client=client,
        table_name=os.getenv("DYNAMO_TABLE"),
        pk="correlationId",
        data={
            "correlationId": "cor123",
            "payload": {
                "message": "Hello World",
                "src": "dynamoDb"
            }
        }
    )
    return context


@mock_dynamodb2
def test_dynamodb_init(monkeypatch, context):
    client = context.client
    monkeypatch.setenv("DYNAMO_TABLE", "TestTable")
    table = client.create_table(
        TableName=os.getenv("DYNAMO_TABLE"),
        KeySchema=[
            {
                "AttributeName": "correlationId",
                "KeyType": "HASH"
            }],
        AttributeDefinitions=[
            {
                "AttributeName": "correlationId",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput=
        {
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=os.getenv("DYNAMO_TABLE"))

    init = InitDynamoDB(context=context)
    res = init.insert()

    assert res["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_dynamodb2
def test_dynamodb_extraction(monkeypatch, context):
    expected = {'statusCode': 200,
                'body': '{"correlationId": "cor123", "payload": {"message": "Hello World", "src": "dynamoDb"}}',
                'isBase64Encoded': False}
    client = context.client
    monkeypatch.setenv("DYNAMO_TABLE", "TestTable")
    table = client.create_table(
        TableName=os.getenv("DYNAMO_TABLE"),
        KeySchema=[
            {
                "AttributeName": "correlationId",
                "KeyType": "HASH"
            }],
        AttributeDefinitions=[
            {
                "AttributeName": "correlationId",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput=
        {
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=os.getenv("DYNAMO_TABLE"))

    __ = InitDynamoDB(context=context)
    __.insert()

    extractor = ExtractMessageDynamoDB(context=context, decimal_encoder=DecimalEncoder)
    actual = extractor.extract(message_key="cor123")
    assert actual == expected
