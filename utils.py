import matplotlib.pyplot as plt
import networkx as nx

presidents = {
    "TEMER",
    "PUTIN",
    "MERKEL",
    "ZUMA",
    "MACRI",
    "TRUDEAU",
    "TRUMP",
    "NIETO",
    "JINPING",
    "ABE",
    "JAE-IN",
    "MODI",
    "WIDODO",
    "SAUD",
    "MACRON",
    "MAY",
    "GENTILONI"
}


def draw_network(graph):
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos=pos)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos=pos, edge_labels=labels)
    plt.show()
