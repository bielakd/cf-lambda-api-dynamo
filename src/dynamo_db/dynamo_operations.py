from .context import SetupDynamoContext
from .helpers import DecimalEncoder
from typing import Type


class InitDynamoDB:
    def __init__(self, context: SetupDynamoContext):
        self.context = context

    def _set_table(self):
        return self.context.client.Table(self.context.table_name)

    def insert(self):
        print(f"---****{self.context.table_name}")
        table = self._set_table()
        print(f"---***{table}")
        response = table.put_item(Item=self.context.data)
        return response


class ExtractMessageDynamoDB:
    def __init__(self, context: SetupDynamoContext, decimal_encoder: Type[DecimalEncoder]):
        self.context = context
        self.encoder = decimal_encoder

    def _set_table(self):
        return self.context.client.Table(self.context.table_name)

    def extract(self, message_key):
        import json
        table = self._set_table()
        try:
            resp = table.get_item(
                Key={self.context.pk: message_key}
            )
            print(f"%%%%---{resp}")
        except Exception(f"Could not retrive data for the key: {message_key}") as ex:
            return {
                "statsCode": 400,
                "body": json.dumps({
                    "error": ex.msg,
                    "errorType": "KEY_RETRIVAL_ERROR"
                }),
                "isBase64Encoded": False
            }
        else:

            item = resp["Item"]
            return {
                "statusCode": 200,
                "body": json.dumps(item, cls=self.encoder),
                "isBase64Encoded": False
            }
