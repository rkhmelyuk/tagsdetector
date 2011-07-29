from pymongo import Connection

class MongoConnection:
    
    def __init__(self, host="localhost", port=27017, database='tags'):
        self.connection = Connection(host=host, port=port)
        self.database = database

    def getDatabase(self):
        return self.connection[self.database]