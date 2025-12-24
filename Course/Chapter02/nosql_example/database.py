from pymongo import MongoClient

client = MongoClient()
# equivalent to
# client = MongoClient("mongodb://localhost:27017")

# In this example, "mydatabase" is the name of your database
database = client.mydatabase

user_collection = database["users"]

