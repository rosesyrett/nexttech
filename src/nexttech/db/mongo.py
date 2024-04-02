from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.cursor import Cursor

from nexttech.settings import Settings, TABLE_NAME
from nexttech.db.error import DoesNotExist
from nexttech.db.feature import Feature
import json

from typing import Dict
import time

def clean_timestamp(value, date_format="%Y-%m-%d") -> int | None:
    if not value:
        return None

    if isinstance(value, str):
        try:
            value = int(float(value))  # '0.0' does not evaluate to integer, 0.0 does
        except ValueError:
            value = int(time.mktime(time.strptime(value, date_format)))

    return abs(value)

class Mongo:
    def __init__(self):
        settings = Settings()
        self.client = MongoClient(f"mongodb+srv://{settings.mongo_atlas_username}:{settings.mongo_atlas_password}@testcluster.pixndsa.mongodb.net/?retryWrites=true&w=majority&appName=TestCluster", server_api=ServerApi('1'))
        self.collection = self.client["next-tech"][TABLE_NAME]

    def _aggregate_features(self, documents: Cursor) -> Dict[str, Feature]:
        features = {}
        last_checked = {}

        for document in documents:
            name = document["name"]
            range_key = document["range_key"]

            if "json:" in range_key:
                last_modified = int(range_key.replace("json:", ""))

                data = json.loads(document["json"])
                for date_key in ["date_start", "date_end"]:
                    correct_timestamp = clean_timestamp(data[date_key])
                    data[date_key] = correct_timestamp

                feature = Feature(**data)
                feature.last_modified = last_modified

                if name not in features:
                    features[name] = [feature]
                else:
                    features[name].append(feature)

            elif "last_checked" in range_key:
                last_checked[name] = int(document["last_checked"])

        collapsed_features = {}

        for name, versions in features.items():
            versions.sort(key=lambda f: f.last_modified, reverse=True)

            latest_version = versions[0]
            latest_version.history = versions[1:]
            latest_version.last_checked = last_checked.get(name)

            collapsed_features[name] = latest_version

        return collapsed_features

    def get(self, feature: str) -> Feature:
        records = self.collection.find({"name":feature})
        features = self._aggregate_features(records)

        if not feature in features:
            raise DoesNotExist(f"{feature} not found")
        return features[feature]
        
    def all(self) -> Dict[str, Feature]:
        records = self.collection.find()
        return self._aggregate_features(records)
