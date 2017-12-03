import networkx as nx
import multiprocessing


class GraphBuilder(object):

    def __init__(self, subject_extractor, preprocessing=None):
        self.graph = nx.Graph()
        self.subject_extractor = subject_extractor
        self.preprocessing = preprocessing

    def build(self, iterable):
        pool = multiprocessing.Pool()
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

                if 'weight' in self.graph[first_subject][second_subject]:
                    self.graph[first_subject][second_subject]['weight'] += 1
                else:
                    self.graph[first_subject][second_subject]['weight'] = 1

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

        for first_subject in subjects_found:
            nodes.add(first_subject)

            for second_subject in subjects_found:
                nodes.add(second_subject)

                if first_subject != second_subject:
                    if (second_subject, first_subject) not in edges:
                        edges.add((first_subject, second_subject))

        return nodes, edges
