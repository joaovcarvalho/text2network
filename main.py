from pymongo import MongoClient
from pymongo.cursor import Cursor
from SubjectsExtractor import SubjectsExtractor
import networkx as nx

DATABASE_NAME = 'socialnetworks'
COLLECTION_NAME = 'estadao'

client = MongoClient('localhost', 27017)
database = client[DATABASE_NAME]

documents_collection = database[COLLECTION_NAME]
cursor = Cursor(documents_collection, no_cursor_timeout=True)

count_documents = cursor.count()
count = 0

graph = nx.Graph()

for element in cursor:
    count += 1
    print(count, "/", count_documents)

    try:
        text = element['Links'][0]['Body']
    except KeyError:
        continue

    subject_extractor = SubjectsExtractor(text)
    subjects_found = subject_extractor.get_named_entities()

    edges = set()

    for first_subject in subjects_found:
        graph.add_node(first_subject)

        for second_subject in subjects_found:
            graph.add_node(second_subject)

            if first_subject != second_subject:
                if (second_subject, first_subject) not in edges:
                    edges.add((first_subject, second_subject))

    for edge in edges:
        first_subject = edge[0]
        second_subject = edge[1]

        graph.add_edge(first_subject, second_subject)

        graph[first_subject][second_subject]['weight'] \
            = graph[first_subject][second_subject].get('weight', 0) + 1

nx.write_gml(graph, COLLECTION_NAME + ".gml")
