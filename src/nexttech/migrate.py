"""Admin script for migrating dynamodb data to mongodb."""

from nexttech.db import Mongo, Dynamo


if __name__ == "__main__":
    mongodb = Mongo()
    dynamodb = Dynamo()

    all_rows = list(dynamodb.iter_scan())
    for row in all_rows:
        # This is needed, as boto3 seems to convert these ints to decimal.Decimal,
        # which can't be serialised into a mongo db document.
        if row["range_key"] == "last_checked":
            row["last_checked"] = int(row["last_checked"])

    mongodb.collection.insert_many(all_rows)
    mongodb.client.close()
