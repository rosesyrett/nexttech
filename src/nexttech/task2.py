from nexttech.db import mongo
db = mongo()
all_documents = db.all()

last_checked_number_list = []

for key,value in all_documents.items():
    last_checked_number_list.append(value.last_checked_number)


print(last_checked_number_list.sort())