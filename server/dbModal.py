import pymongo


class NccAuctionModal:
    def connect(self, col_name):
        connection = pymongo.MongoClient("localhost", 27017)
        database = connection["ncc_dip2"]
        collection = database[col_name]
        return collection

    def item(self):
        collection = self.connect("items_and_prices")
        return collection

    def info(self):
        collection = self.connect("user_info")
        return collection
