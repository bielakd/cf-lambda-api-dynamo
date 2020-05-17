from .context import SetupDynamoContext
from .helpers import DecimalEncoder
from typing import Type

class InitDynamoDB:
    def __init__(self, context: SetupDynamoContext):
        self.context = context

    def _set_table(self):
        return self.context.client.Table(self.context.table_name)

    def insert(self):
        table = self._set_table()
        response = table.put_item(Item={self.context.data})
        return response


class ExtractMessageDynamoDB:
    def __init__(self, context: SetupDynamoContext, decimal_encoder: Type[DecimalEncoder]):
        self.context = context
        self.encoder = decimal_encoder

    def _set_table(self):
        return self.context.client.Table(self.context.table_name)

    def extract(self, message_key):
        table = self._set_table()
        resp = table.get_item(
            Key={self.context.pk: message_key}
        )
        self._extract_message(response=resp)

    def _extract_message(self, response):
        try:
        except Exception as ex:
            return ex
        else:
            import json
            item = response["Item"]
            return json.dumps(item, cls=self.encoder)



