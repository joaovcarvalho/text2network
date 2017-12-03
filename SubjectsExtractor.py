import nltk
from nltk.chunk import conlltags2tree, tree2conlltags


class SubjectsExtractor(object):

    def __init__(self, text, language="portuguese"):
        self.language = language
        self.text = text

    def get_named_entities(self, entity_type="GPE"):
        tags = self.get_text_tagged()

        ne_tree = nltk.ne_chunk(tags)

        iob_tagged = tree2conlltags(ne_tree)
        ne_tree = conlltags2tree(iob_tagged)

        return [" ".join(map(lambda x: x[0], node.leaves())) for node in ne_tree
                if type(node) == nltk.tree.Tree and node.label() == entity_type]

    def get_text_tagged(self):
        tokens = nltk.word_tokenize(self.text, language=self.language)
        tags = nltk.pos_tag(tokens)
        return tags

    def get_elements_from_allowed_list(self, allowed_list, tag_type="NN"):
        tags = self.get_text_tagged()

        subjects_found = [tag[0].upper() for tag in tags if tag[1] == tag_type and tag[0].upper() in allowed_list]
        return subjects_found

