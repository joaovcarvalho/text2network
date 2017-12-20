# Text2Network
This projects aims to provide a library to creating network graphs based 
on groups of texts. 

It uses the Dbpedia Spotlight to extract known named entities from text
and connect them in a social network.

## Usage

Example using a Mongo Database to provide the texts:

```python
def preprocessing(x):
    print("Processing: ", x['Links'][0]['Uri'])
    return x['Links'][0]['Body']


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    database = client[DATABASE_NAME]

    documents_collection = database[COLLECTION_NAME]
    cursor = Cursor(documents_collection, no_cursor_timeout=True)

    graph_builder = GraphBuilder(DbpediaSubjectsExtractor, preprocessing=preprocessing)
    graph_builder.build(cursor)
    graph_builder.save_graph(COLLECTION_NAME + ".gml")
```