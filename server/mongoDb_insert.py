import pymongo
import random

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
collection = database["items_and_prices"]

for i in range(5):
    item = "car" + str(i)
    price = random.randint(1000, 10000000)
    data_form: dict = {"name": item, "reserve_price": price}
    ids = collection.insert_one(data_form)
    print(ids.inserted_id)
