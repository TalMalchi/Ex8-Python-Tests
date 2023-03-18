import unittest

import networkx as nx

from src.Agent import Agent
from src.Pokemon import Pokemon
from src.timeStampsDemo import *
from unittest import TestCase


def initGraph():
    graph = nx.DiGraph()
    from src.Point import Point
    graph.add_node(0, pos=Point(0, 0, 0))
    graph.add_node(1, pos=Point(1, 0, 0))
    graph.add_node(2, pos=Point(2, 0, 0))
    graph.add_node(3, pos=Point(3, 0, 0))
    graph.add_node(4, pos=Point(4, 0, 0))

    graph.add_edge(0, 1, weight=2)
    graph.add_edge(1, 2, weight=2)
    graph.add_edge(2, 3, weight=2)
    graph.add_edge(3, 4, weight=2)
    graph.add_edge(4, 3, weight=2)
    graph.add_edge(3, 2, weight=2)
    graph.add_edge(2, 1, weight=2)
    graph.add_edge(1, 0, weight=2)

    pok1 = Pokemon(graph, value=2, type=1, pos=Point(1 / 3, 0, 0))
    pok2 = Pokemon(graph, value=2, type=1, pos=Point(2.5, 0, 0))
    pok3 = Pokemon(graph, value=2, type=1, pos=Point(4.75, 0, 0))

    agent = Agent(id=0, value=1, src=0, dest=1, speed=2, pos=Point(0, 0, 0))

    timestamps = initialTimeStamps([], graph, agent)
    return timestamps


print(initGraph())

if __name__ == '__main__':
    unittest.main()