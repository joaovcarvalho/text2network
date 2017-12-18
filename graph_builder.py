import networkx as nx
import multiprocessing
import itertools

WEIGHT_KEY_IN_DICT = 'weight'
COMBINATIONS_OF = 2


class GraphBuilder(object):

    def __init__(self, subject_extractor, preprocessing=None):
        self.graph = nx.Graph()
        self.subject_extractor = subject_extractor
        self.preprocessing = preprocessing

    def build(self, iterable):
        multiprocessing.freeze_support()
        pool = multiprocessing.Pool(8)
        subgraphs = pool.map(self.process_element, iterable)

        for subgraph in subgraphs:

            try:
                (nodes, edges) = subgraph
            except TypeError:
                continue

            self.graph.add_nodes_from(nodes)

            for edge in edges:
                first_subject = edge[0]
                second_subject = edge[1]

                self.graph.add_edge(first_subject, second_subject)

                if WEIGHT_KEY_IN_DICT not in self.graph[first_subject][second_subject]:
                    self.graph[first_subject][second_subject][WEIGHT_KEY_IN_DICT] = 1

                self.graph[first_subject][second_subject][WEIGHT_KEY_IN_DICT] += 1

    def save_graph(self, path):
        nx.write_gml(self.graph, path)

    def process_element(self, element):
        try:
            if self.preprocessing is None:
                text = element
            else:
                text = self.preprocessing(element)

        except KeyError:
            return

        subject_extractor = self.subject_extractor(text)
        subjects_found = subject_extractor.get_named_entities()

        edges = set()
        nodes = set()

        for node in subjects_found:
            nodes.add(node)

        for edge in itertools.combinations(subjects_found, COMBINATIONS_OF):
            edges.add(edge)

        return nodes, edges
