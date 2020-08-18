from config.config import Config
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
import urllib.parse

user = urllib.parse.quote(Config.get('db_user'))
password = urllib.parse.quote(Config.get('db_password'))

host = Config.get('db_host')
db_name = Config.get('db_name')

MONGO_URI = f'mongodb+srv://{user}:{password}@{host}/{db_name}?retryWrites=true&w=majority'


class MongoLib:
    """Helper class for generic MongoDB CRUD operations"""
    def __init__(self):
        client = MongoClient(MONGO_URI)
        self.db = client[db_name]

    def get_all(self, collection, query={}, limit=0):
        """Returns all objects matching 'query' in database sorted by insertion date"""
        collection = self.db[collection]
        return collection.find(query, limit=limit).sort('_id', DESCENDING)

    def get(self, collection, id):
        """Returns a single object with given ID"""
        collection = self.db[collection]
        return collection.find_one({'_id': ObjectId(id)})

    def insert(self, collection, document):
        """Inserts document into database and returns the inserted object ID"""
        collection = self.db[collection]
        return str(collection.insert_one(document).inserted_id)

    def update(self, collection, id, data):
        """Updates document from database and returns the number of modified documents, if any"""
        collection = self.db[collection]
        collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        return id

    def delete(self, collection, id):
        """Deleted document from database and returns the deleted object ID"""
        collection = self.db[collection]
        collection.delete_one({'_id': ObjectId(id)})
        return id







