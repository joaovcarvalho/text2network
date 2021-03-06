import nltk
import pickle
from nltk.chunk import conlltags2tree, tree2conlltags
from unicodedata import normalize

BLACK_LIST = {
    "EU",
    "OS",
    "POR",
    "UMA",
    "ACHO",
    "CADA",
    "UM",
    "EM",
    "PARA",
    "PORTANTO",
    "SERIA",
    "NA",
    "NORMALMENTE",
    "DE",
    "SEM",
    "CIDADE",
    "ESTÁDIO",
    "ESTADO",
    "FOI",
    "QUEM",
    "ELE",
    "ESSE",
    "DEPOIS",
    "MAIS",
    "NOS",
    "NUMA",
    "TODOS",
    "FORA",
    "ENTRE",
    "NUM",
    "HOJE"
}


class SubjectsExtractor(object):

    def __init__(self, text, language="portuguese"):
        self.language = language
        self.text = text
        self.portuguese_tagger = pickle.load(open("tagger.pkl", "rb"))
        self.tagger = nltk.pos_tag

    def _get_name_entities(self, tags):
        ne_tree = nltk.ne_chunk(tags)
        iob_tagged = tree2conlltags(ne_tree)
        ne_tree = conlltags2tree(iob_tagged)
        return ne_tree

    def get_named_entities(self, entity_type="PERSON"):
        tags = self.get_text_tagged()
        ne_tree = self._get_name_entities(tags)

        result = set()
        for node in ne_tree:
            if type(node) == nltk.tree.Tree and node.label() == entity_type:
                leaves = list(map(lambda x: x[0], node.leaves()))

                # Portuguese checking
                leaves = map(lambda x: x[0], filter(lambda x: x[1] == 'NOUN', self.portuguese_tagger.tag(leaves)))

                graph_node = " ".join(leaves).upper()
                if graph_node not in BLACK_LIST and graph_node != '':
                    # replace accentuations
                    graph_node = normalize('NFKD', graph_node).encode('ASCII', 'ignore').decode('ASCII')
                    result.add(graph_node)

        return result

    def get_text_tagged(self):
        tokens = nltk.word_tokenize(self.text, language=self.language)
        tags = self.tagger(tokens)
        return tags

    def get_elements_from_allowed_list(self, allowed_list, tag_type="NN"):
        tags = self.get_text_tagged()

        subjects_found = [tag[0].upper() for tag in tags if tag[1] == tag_type and tag[0].upper() in allowed_list]
        return subjects_found

