import pytest
import app
import json


def test_app_import():
    expected = {'body': json.dumps({"payload": "Hello World"}), 'isBase64Encoded': False, 'statusCode': 200}
    actual = app.handler(event=1, context="")

    assert actual == expected
