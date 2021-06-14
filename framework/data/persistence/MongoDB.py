from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config.DbConfig import DbConfig
from framework.util.logger.Log import Log


class MongoDB:

    user_name = ''
    passwd = ''
    db_name = ''
    host_name = ''
    port = ''
    db = ''

    def __init__(self):
        self.host_name = DbConfig.HOSTNAME
        self.port = DbConfig.PORT
        self.user_name = DbConfig.HOSTNAME
        self.passwd = DbConfig.PASSWORD
        self.db_name = DbConfig.DBNAME

    def create_client(self):
        client = MongoClient(self.host_name, self.port)
        return client

    def get_db(self):
        client = self.create_client()
        db = client[self.db_name]
        return db

    def get_collection(self, collection_name):
        db = self.get_db()
        coll = db[collection_name]
        return coll

    def insert_one(self, collection_name, document):
        try:
            coll = self.get_collection(collection_name)
            doc_id = coll.insert_one(document)
            return doc_id
        except DuplicateKeyError as dupexcep:
            Log.warning('Duplicate Key: Insert Failed!')
            Log.warning('Exception: {0}'.format(dupexcep))
        except Exception as excep:
            Log.fatal('Insert Failed!')
            Log.fatal('Exception: {0}'.format(excep))
            exit(1)

    def insert_many(self, collection_name, documents):
        try:
            coll = self.get_collection(collection_name)
            doc_id = coll.insert_many(documents)
            return doc_id
        except DuplicateKeyError as dupexcep:
            Log.warning('Duplicate Key: Insert Failed!')
            Log.warning('Exception: {0}'.format(dupexcep))
        except Exception as excep:
            Log.fatal('Insert Failed!')
            Log.fatal('Exception: {0}'.format(excep))
            exit(1)

    def find_one(self, collection_name, query):
        try:
            coll = self.get_collection(collection_name)
            result = coll.find_one(query)
            return result
        except Exception as excep:
            Log.fatal('Select Failed!')
            Log.fatal('Exception: {0}'.format(excep))
            exit(1)

    def find_many(self, collection_name, query):
        try:
            coll = self.get_collection(collection_name)
            result = coll.find(query)
            return result
        except Exception as excep:
            Log.fatal('Select Failed!')
            Log.fatal('Exception: {0}'.format(excep))
            exit(1)

    def find_count(self, collection_name, query):
        try:
            coll = self.get_collection(collection_name)
            count = coll.find(query).count()
            return count
        except Exception as excep:
            Log.fatal('Select Failed!')
            Log.fatal('Exception: {0}'.format(excep))
            exit(1)

    # TODO: Write UD for MongoDB
