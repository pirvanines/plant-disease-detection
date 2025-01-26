from pymongo import MongoClient

class Databse():
    def __init__(self, client, colectie):
        self.client = MongoClient('mongodb://localhost:27017/')

        self.db = self.client[client]
        self.colectie = self.db[colectie]

    def InsertDocument(self, document):
        rezultat = self.colectie.insert_one(document)

    def ParcurgeDocumente(self):
        for doc in self.colectie.find():
            print(doc)

    def NumElements(self):
        return self.colectie.count_documents({})
    
    def FindElement(self, filtru):
        return self.colectie.find_one(filtru)
    
    def DeleteElement(self, filtru):
        self.colectie.delete_one(filtru)
        