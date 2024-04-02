from nexttech.db.mongo import clean_timestamp, Mongo
import mock
import os

def test_clean_timestamp():
    assert clean_timestamp("1712064693.2184472") == 1712064693

# Mock out the mongo client so this test doesn't actually connect to a database,
@mock.patch("pymongo.mongo_client.MongoClient")
def test_aggregate_features(mongo_client, monkeypatch):
    # set environment variables needed to construct the right URL
    monkeypatch.setattr(os, 'environ', {"MONGO_ATLAS_USERNAME": "foo", "MONGO_ATLAS_PASSWORD": "bar"})

    db = Mongo()

    features = [
        {
            "name": "abc",
            "range_key": "json:123456",
            "json": '{\"id\":\"1\", \"name\": \"abc\", \"desc\":\"...\", \"last_editor\":\"someone\", \"last_checked\":123456, \"last_modified\": 123456, \"date_start\": null, \"date_end\": null}'
        },
        {
            "name": "def",
            "range_key": "json:123456",
            "json": '{\"id\":\"2\", \"name\": \"abc\", \"desc\":\"...\", \"last_editor\":\"someone\", \"last_checked\":123456, \"last_modified\":789101112, \"date_start\": null, \"date_end\": null}'
        },
        {
            "name": "abc",
            "range_key": "last_checked",
            "last_checked": 789101112
        }
    ]

    def fake_feature_iterator():
        for feature in features:
            yield feature

    aggregated = db._aggregate_features(fake_feature_iterator())

    assert aggregated["abc"].last_checked == 789101112