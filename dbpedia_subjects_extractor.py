from unicodedata import normalize
import spotlight
from functools import *
import requests


class DbpediaSubjectsExtractor(object):
    def __init__(self, text, language="portuguese"):
        self.language = language
        self.text = text

    def get_named_entities(self, entity_type="PERSON"):

        try:
            annotations = spotlight.annotate('http://model.dbpedia-spotlight.org/pt/annotate',
                                             self.text,
                                             confidence=0.4, support=20)
        except (ValueError,
                spotlight.SpotlightException,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError):
            return []

        allowed_types = {"Schema:Person", "DBpedia:Person", "Http://xmlns.com/foaf/0.1/Person"}

        result = set()
        for annotation in annotations:
            types = set(annotation["types"].split(","))

            is_person = reduce(lambda x, y: x or y, [a in types for a in allowed_types])
            if is_person:
                graph_node = annotation["surfaceForm"].upper()
                graph_node = normalize('NFKD', graph_node).encode('ASCII', 'ignore').decode('ASCII')
                result.add(graph_node)

        return result
