from nexttech.db.mongo import Mongo
import datetime
db = Mongo()
all_documents = db.all()

def firstvalue(numbername):
    return numbername[0]


modified_features = []

for feature_name,feature_data in all_documents.items():
    modified_features.append((feature_data.last_modified,feature_name))


modified_features.sort(key=firstvalue)
# print(modified_features)
print(modified_features[0])

epoch_time = modified_features[0][0]
date_time = datetime.datetime.fromtimestamp(epoch_time)
print("converted epoch time",date_time)

