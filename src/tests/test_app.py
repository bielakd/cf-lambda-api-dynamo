import pytest
import app


def test_app_import():
    expected = {'Hello': 'World', 'isBase64Encoded': False}
    actual = app.handler(event=1, context="")

    assert actual == expected
