from pymongo import MongoClient
from pymongo.cursor import Cursor
from GraphBuilder import GraphBuilder
from SubjectsExtractor import SubjectsExtractor

DATABASE_NAME = 'socialnetworks'
COLLECTION_NAME = 'estadao'

client = MongoClient('localhost', 27017)
database = client[DATABASE_NAME]

documents_collection = database[COLLECTION_NAME]
cursor = Cursor(documents_collection, no_cursor_timeout=True).limit(20)

def preprocessing(x):
    print("Processing: ", x['Links'][0]['Uri'])
    return x['Links'][0]['Body']

graph_builder = GraphBuilder(SubjectsExtractor, preprocessing=preprocessing)
graph_builder.build(cursor)
graph_builder.save_graph(COLLECTION_NAME + ".gml")
