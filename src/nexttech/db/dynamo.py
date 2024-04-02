"""Sets up database connection to aws table"""

import boto3
from nexttech.settings import TABLE_NAME, DYNAMODB_ENDPOINT_URL


class Dynamo:
    def __init__(self):
        self._ddb = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT_URL)
        self._table = self._ddb.Table(TABLE_NAME)

    def iter_scan(self, **kwargs):
        response = self._table.scan(**kwargs)

        yield from response["Items"]

        while "LastEvaluatedKey" in response:
            response = self._table.scan(
                ExclusiveStartKey=response["LastEvaluatedKey"],
                **kwargs,
            )

            yield from response["Items"]
