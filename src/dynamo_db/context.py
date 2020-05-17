from collections import namedtuple


SetupDynamoContext = namedtuple("DynamoContext",
                           [
                               "client",
                               "table_name",
                               "data",
                               "pk"
                           ])