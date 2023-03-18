import json
import unittest
from unittest import TestCase
from src.Pokemon import Pokemon
import networkx as nx
from src.Point import Point


class test_Pokemon(TestCase):
    def test_parse_pok(self):
        graph = nx.DiGraph()
        pok = Pokemon(graph)
        s = json.loads('{"Pokemons":[{"Pokemon":{"value":5.0,"type":-1,"pos":"35.197656770719604,32.10191878639921,0.0"}}]}')['Pokemons'][0]
        pok.parsePokemon(s)
        pok_tocheck = Pokemon(graph, 5.0, -1, Point(35.197656770719604, 32.10191878639921, 0.0))
        self.assertEqual(pok, pok_tocheck)

    def test_find_src_dest(self):
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        p= Pokemon(graph, 0, 1, Point(1.5 , 0, 0))
        #def __init__(self, graph: nx.DiGraph, value=0, type: int = 0, pos: Point = Point(), jsonStr=None):
        p.findSrcDest(graph)
        self.assertEqual(p.node_dest,3)
        self.assertEqual(p.node_src,2)

    def test_get_set_value(self):
        graph1 = nx.DiGraph()
        p = Pokemon(graph1, 0, 1, Point(1, 2, 0))
        self.assertEqual(p.getValue(), 0)
        p.setValue(4)
        self.assertEqual(p.getValue(), 4)
        p1 = Pokemon(graph1, 4, 1, Point(1, 2, 0))
        p.setValue(1)
        self.assertEqual(p.getValue(), 1)

    def test_get_set_type(self):
        graph1 = nx.DiGraph()
        p = Pokemon(graph1, 0, 1, Point(1, 2, 0))
        self.assertEqual(p.getType(), 1)
        p.setType(-1)
        self.assertEqual(p.getType(), -1)


    def test_get_set_pos(self):
        graph1 = nx.DiGraph()
        p = Pokemon(graph1, 0, 1, Point(1, 2, 0))
        self.assertEqual(p.pos.getX(), 1)
        self.assertEqual(p.pos.getZ(), 0)
        p.setPos(Point(1, 4, 5))
        self.assertEqual(p.pos.getZ(), 5)

    def test_get_node_src(self):
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        p = Pokemon(graph, 0, 1, Point(1.5, 0, 0))
        ans=p.get_node_src()
        self.assertEqual(ans, 2)

    def test_get_node_dest(self):
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        p = Pokemon(graph, 0, 1, Point(1.5, 0, 0))
        ans = p.get_node_dest()
        self.assertEqual(ans, 3)

if __name__ == '__main__':
    unittest.main()