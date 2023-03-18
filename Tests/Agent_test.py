import json
import time
import unittest
from unittest import TestCase

from networkx import *

from src.Agent import Agent
from src.Point import Point
from src.Pokemon import Pokemon


class test_Agent(TestCase):

    def test_parse_agent(self):  # TODO
        ag = Agent()
        s1 = json.loads('{"Agents":[{"Agent":{"id":0,"value":0.0,"src":0,"dest":1,"speed":1.0,"pos":"35.18753053591606,32.10378225882353,0.0"}}]}')['Agents'][0]['Agent']
        ag.parseAgent(s1)
        agent_toCheck = Agent(0, 0.0, 0, 1, 1.0, Point(35.18753053591606, 32.10378225882353, 0.0))
        self.assertEqual(ag, agent_toCheck)

    def test_set_previous_node_time(self):
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.set_previous_node_time(5.0)
        ans = a.get_previous_node_time()
        self.assertEqual(ans, 5.0)

    def test_set_pos_vchange(self):
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.set_pos_Vchange(Point(1, 2, 0))
        ans = a.get_pos_Vchange()
        self.assertEqual(ans, Point(1, 2, 0))

    # def test_get_pos_vchange(self):
    #     assert False

    def test_get_id(self):
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        ans = a.getId()
        self.assertEqual(ans, 0)

        #    def __init__(self, graph: nx.DiGraph, value=0, type: int = 0, pos: Point = Point(), jsonStr=None): pokemin

        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent

    def test_get_value(self):
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent

        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        ans = a.getValue()
        self.assertEqual(ans, 1)

    def test_set_value(self):
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.setValue(10)
        ans = a.getValue()
        self.assertEqual(ans, 10)

    def test_get_speed(self):
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        ans = a.set_speed(22)  # .setValue(10)
        ans = a.get_speed()
        self.assertEqual(ans, 22)

    # def test_set_speed(self):
    #     assert False

    # def test_get_pos(self):
    #     assert False

    def test_set_pos(self):
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.setPos((1, 2, 0))  # .setValue(10)
        ans = a.getPos()
        self.assertEqual(ans, Point(1, 2, 0))

    # def test_get_src(self):
    #     assert False

    def test_set_src(self):
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.setPos((1, 2, 0))  # .setValue(10)
        a.setSrc(5)
        ans = a.getSrc()
        self.assertEqual(ans, 5)

    # def test_get_dest(self):
    #     assert False

    def test_set_dest(self):
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.setPos((1, 2, 0))  # .setValue(10)
        a.setDest(7)
        ans = a.getDest()
        self.assertEqual(ans, 7)

    def test_add_to_path(self):  # TODO
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(1, 3, weight=1)
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.path = []
        current = time.time()
        current1 = time.time()
        a.addToPath([5], graph, [current, current1])
        ans = a.getPathHead()
        self.assertEqual(ans, 5)

    def test_get_path_head(self):
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent

        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.set_previous_node_time(time.time())
        a.set_pos_Vchange(Point(0, 0, 0))
        a.path = [1, 2, 3]
        ans = a.getPathHead()
        self.assertEqual(ans, 1)

    def test_remove_path_head(self):
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.set_previous_node_time(time.time())
        a.set_pos_Vchange(Point(0, 0, 0))
        a.path = [1, 2, 3]
        a.removePathHead()
        ans = a.getPathHead()
        self.assertEqual(ans, 2)

    def test_get_path(self):
        graph = nx.DiGraph()

        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent
        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.set_previous_node_time(time.time())
        a.set_pos_Vchange(Point(0, 0, 0))
        a.setPath([1, 2, 3], [], graph, [])
        #    def setPath(self, path: list, lstToAdd: list, graph: nx.DiGraph, timeStamps: list):

        ans = a.getPath()
        self.assertEqual(ans, [1, 2, 3])

    # def test_set_path(self):
    #   assert False

    def test_get_pok_lst(self):
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(1, 3, weight=1)
        p1 = Pokemon(graph, 0, 1, Point(1, 2, 1))
        p2 = Pokemon(graph, 1, 1, Point(1, 2, 2))
        p3 = Pokemon(graph, 2, 1, Point(1, 2, 3))
        print(p1)

        # poke_list = [p1, p2, p3]
        poke_list1 = []
        poke_list1.append(Pokemon(graph, 0, 1, Point(1, 2, 1)))
        poke_list1.append(Pokemon(graph, 1, 1, Point(1, 2, 2)))
        poke_list1.append(Pokemon(graph, 2, 1, Point(1, 2, 3)))

        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.setPokLst(poke_list1)
        ans = a.getPokLst()
        self.assertEqual(ans, poke_list1)

    def test_get_pok_lst_head(self):
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(1, 3, weight=1)

        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        poke_list1 = []
        poke_list1.append(Pokemon(graph, 0, 1, Point(1, 2, 1)))
        poke_list1.append(Pokemon(graph, 1, 1, Point(1, 2, 2)))
        poke_list1.append(Pokemon(graph, 2, 1, Point(1, 2, 3)))
        a.setPokLst(poke_list1)
        ans = a.getPokLstHead()

        self.assertEqual(ans, Pokemon(graph, 0, 1, Point(1, 2, 1)))

    # def test_set_pok_lst(self):
    #     assert False

    # def test_add_pokemons_list_per_agent(self):
    #   assert False

    def test_add_time_stamps(self):  # TODO
        assert False

    def test_find_curr_pos_of_agent(self):  # TODO
        # (self, graph: nx.DiGraph)
        # test without changing speed
        graph = nx.DiGraph()
        graph.add_node(1, pos=Point(0, 0, 0))
        graph.add_node(2, pos=Point(1, 0, 0))
        graph.add_node(3, pos=Point(2, 0, 0))
        graph.add_edge(1, 2, weight=1)
        graph.add_edge(2, 3, weight=1)
        graph.add_edge(1, 3, weight=1)
        # (self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0,Point = Point(), jsonStr=None): #agent

        a = Agent(0, 1, 1, 2, 1, Point(0, 0, 0))
        a.set_previous_node_time(time.time())
        a.set_pos_Vchange(Point(0, 0, 0))
        a.path = [1, 2, 3]
        time.sleep(0.5)

        ans = a.find_curr_pos_of_agent(graph)
        self.assertEqual(ans, (0.5, 0, 0))

        # # test with changing speed
        # A = Agent(0, 1, 1, 2, 0.5, Point(1, 2, 0))
        # A.set_speed(2)
        # # p = Pokemon(graph, 0, 1, Point(1, 2, 0))

if __name__ == '__main__':
    unittest.main()