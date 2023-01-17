# TDP015 Programming Assignment 5
# Graphs
# Skeleton Code

import sys
# In a research project at IDA algorithms
# for the parsing of natural language to meaning representations in
# the form of directed graphs are developed:
#
# http://www.ida.liu.se/~marku61/ceniit.shtml
#
# A desirable property of these graphs is that they should be acyclic,
# that is, should not contain any (directed) cycles. Your task in this
# assignment is to implement a Python function that tests this
# property, and to apply your function to compute the number of cyclic
# graphs in one of the datasets that I am using in my research.
#
# Your final script should be callable from the command line as follows:
#
# $ python3 p5.py ccg.train.json
#
# With this data file your program should report 418 cyclic graphs.
#
# The graphs are stored in a JSON file containing a single dictionary
# mapping graph ids (8-digit integers) to graphs, where each graph is
# represented as a dictionary mapping vertices (or rather their ids)
# to lists of neighbouring vertices.


def cyclic(graph):
    """Test whether the directed graph `graph` has a (directed) cycle.

    The input graph needs to be represented as a dictionary mapping vertex
    ids to iterables of ids of neighboring vertices. Example:

    {"1": ["2"], "2": ["3"], "3": ["1"]}

    Args:
        graph: A directed graph.

    Returns:
        `True` iff the directed graph `graph` has a (directed) cycle.
    """
    deg = {d: 0 for d in graph.keys()}
    for neighbours in graph.values():
        for neighbour in neighbours:
            deg[neighbour] += 1

    self = [k for k, v in deg.items() if v == 0]

    nodeNum = 0
    while(len(self) > 0):
        nodeNum += 1
        node = self.pop(0)
        for neighbour in graph[node]:
            deg[neighbour] -= 1
            if deg[neighbour] == 0:
                self.append(neighbour)

    return len(graph) - nodeNum > 2


if __name__ == "__main__":
    opener = eval(open(sys.argv[1], 'r').read())
    for graphNum in opener:
        if cyclic(opener[graphNum]):
            print(graphNum)
            print(opener[graphNum])
