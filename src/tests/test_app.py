import pytest
import app
import json

@pytest.mark.skip(reason="Integration test requires the table to exists in AWS env.")
def test_app_import(monkeypatch):
    monkeypatch.setenv("DYNAMO_TABLE", "TestTable")
    expected_keys = ['statusCode', 'body', 'isBase64Encoded']

    resp = app.handler(event=1, context="")
    actual_keys = list(resp.keys())
    assert actual_keys == expected_keys
