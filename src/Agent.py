import math
import time

import networkx as nx

from src.Point import Point
from src.Pokemon import Pokemon


def quadratic(a, b, c):  # (self, a, b, c):
    """Method to calculate the results of a quadratic equation (2 values)"""
    x1 = ((-b) + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = ((-b) - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return x1, x2


class Agent:

    def __init__(self, id: int = 0, value: float = 0, src: int = 0, dest: int = 0, speed: float = 0, pos: Point = Point(), jsonStr=None):
        self.pokList = []
        if jsonStr is not None:
            self.parseAgent(jsonStr)
        else:
            self.id = id
            self.value = value  # how many did the agent eat till now
            self.dest = dest
            self.src = src
            self.speed = speed
            self.pos = pos
            # Do Not add anything else to "else"
        self.prevNodeTime = 0  # this is the time that passed from the start of travel from previous node
        self.path = []
        self.passedPokPos = Point()  # this is the position that the agent changed his speed or its prev node (whichever was last)

    def parseAgent(self, jsonStr):
        """Function receives json object of pokemon and parses it, assigning values to current pokemon"""
        self.id = jsonStr['id']
        self.value = jsonStr['value']
        self.src = jsonStr['src']
        self.dest = jsonStr['dest']
        self.speed = jsonStr['speed']
        self.pos = Point(string=jsonStr['pos'])

    def _str_(self):
        return "{id: " + str(self.id) + ", value: " + str(self.value) + ", src: " + str(self.src) + ", dest: " + str(
            self.dest) + ", speed: " + str(self.speed) + ", pos: " + str(self.pos) + ", path: " + str(self.path)

    def _repr_(self):
        return self._str_()

    def get_previous_node_time(self):
        """the time that passed from the start of travel from previous node"""
        return self.prevNodeTime

    def set_previous_node_time(self, previous_node_time):
        """set the time that passed from the start of travel from previous node"""
        self.prevNodeTime = previous_node_time

    def setPassedPokPos(self, passedPokPos: Point):
        """set the position that the agent changed his speed"""
        self.passedPokPos = passedPokPos

    def getPassedPokPos(self) -> Point:
        """get the position that the agent changed his speed"""
        return self.passedPokPos

    def getId(self):
        """get the id of the agent"""
        return self.id

    def getValue(self):
        """get the value of the agent"""
        return self.value

    def setValue(self, val):
        """set the value of the agent"""
        self.value = val

    def get_speed(self):
        """get the speed of the agent"""
        return self.speed

    def set_speed(self, sp):
        """set the speed of the agent"""
        self.speed = sp

    def getPos(self):
        return self.pos

    def setPos(self, pos):
        self.pos = pos

    def getSrc(self):
        return self.src

    def setSrc(self, src):
        self.src = src

    def getDest(self):
        return self.dest

    def setDest(self, dest):
        self.dest = dest

    def addToPath(self, lst: list):
        """Set the path the agent needs to move on to get the pokemon as fast as he can"""
        for i in lst:
            self.path.append(i)

    def getPathHead(self):
        return self.path[0]

    def removePathHead(self):
        temp = self.path[0]
        self.path.pop(0)
        return temp

    def getPath(self):
        """Get the path the agent need to move on to get the pokemon as fast as he can"""
        return self.path

    def setPath(self, path: list):
        self.path = path

    def getPokLst(self):
        """get the list of pokemons for each agent"""
        return list(self.pokList)

    def getPokLstHead(self) -> Pokemon:
        """get the list of pokemons for each agent"""
        return self.pokList[0]

    def setPokLst(self, PokemonsListPerAgent: list):
        self.pokList = PokemonsListPerAgent

    def addToPokList(self, pok: Pokemon):
        self.pokList.append(pok)

    def popHeadPokLst(self) -> Pokemon:
        """function get the head of pokList"""
        return self.pokList.pop(0)

    # def addTimeStamps(self, graph: nx.DiGraph, timeStamps: list):
    #     """timestamps := list of the timestamps when the 'move' method from client should be called"""
    #     for timeId in range(len(timeStamps)):  # Remove existing timestamps of current agent
    #         if timeStamps[timeId][1] == self.id:
    #             timeStamps.pop(timeId)
    #             timeId -= 1
    #     for i in range(len(self.path) - 1):  # go all over the agent's path
    #         pokFound = False
    #         for pok in self.pokList:
    #             if self.path[i] == pok.node_src and self.path[i + 1] == pok.node_dest:  # if the next edge has a pokemmon
    #                 # Currently, the assumption is that there are no 2 pokemons on 1 edge
    #                 pokFound = True  # pokemon found
    #                 dist_src_dst = graph.nodes[pok.get_node_src()]['pos'].distance(graph.nodes[pok.get_node_dest()][
    #                                                                                    'pos'])  # total distance of the edge
    #                 dist_pokemon_src = graph.nodes[pok.get_node_src()]['pos'].distance(
    #                     pok.getPos())  # distance between src node to pokemon
    #                 percentOfEdgePassedTillPokemon = dist_pokemon_src / dist_src_dst
    #                 time_to_pokemon = percentOfEdgePassedTillPokemon * (
    #                         graph.get_edge_data(pok.get_node_src(), pok.get_node_dest())['weight'] / self.speed)  # total time to pass the distance from src to pokemon
    #                 percentOfEdgePassedFromPokemon = 1 - percentOfEdgePassedTillPokemon
    #                 time_from_pokemon = percentOfEdgePassedFromPokemon * (
    #                         graph.get_edge_data(pok.get_node_src(), pok.get_node_dest())['weight'] / self.speed)  # total time to pass the distance from pokemon to dest
    #                 if len(timeStamps) >= 1:
    #                     lastElement = timeStamps[-1][0]
    #                 else:
    #                     lastElement = 0
    #                 timeStamps.append((lastElement + time_to_pokemon, self.id))  # add the time to timeStamps list
    #                 timeStamps.append((lastElement + time_from_pokemon, self.id))
    #                 break
    #         if pokFound is False:  # if pokemon hasn't been found on the edge
    #             timeToNextNode = graph.get_edge_data(self.path[i], self.path[i + 1])['weight'] / self.speed  # total time to the next node
    #             if len(timeStamps) >= 1:
    #                 timeStamps.append((timeStamps[-1][0] + timeToNextNode, self.id))  # add the time to timeStamps list
    #             else:
    #                 timeStamps.append((timeToNextNode, self.id))
    #     sorted(timeStamps, key=lambda x: x[0])
    #     return timeStamps
    #
    # def distanceFromSrcNode(self, graph: nx.DiGraph):
    #     """" check the current position of the agent """
    #     timeFromStart = time.time() - self.prevNodeTime
    #     lengthOfEdge = graph.nodes[self.path[0]]['pos'].distance(graph.nodes[self.path[1]]['pos'])
    #     if (not (self.getPokLstHead().node_src == self.path[0] and self.getPokLstHead().node_dest == self.path[1])) or \
    #             (self.pokList[0].get_node_src() == self.path[0] and self.pokList[0].get_node_dest() == self.path[1]):
    #         # No pokemon on current edge or agent before pokemon on current edge
    #         percentOfEdge = timeFromStart / (graph.get_edge_data(self.path[0], self.path[1])['weight'] / self.speed)
    #         return lengthOfEdge * percentOfEdge
    #     else:
    #         # Pokemon passed on current edge
    #         srcPokDist = self.passedPokPos.distance(graph.nodes[self.path[0]]['pos'])
    #         newEdgeLength = lengthOfEdge - srcPokDist
    #         newWeight = graph.get_edge_data(self.path[0], self.path[1])['weight'] * (newEdgeLength / lengthOfEdge)
    #         percentOfEdge = timeFromStart / (newWeight / self.speed)
    #         return newEdgeLength * percentOfEdge
    #
    # def find_curr_pos_of_agent(self, graph: nx.DiGraph) -> Point:
    #     """function get agent and return his current position (Point)"""
    #     xStart = graph.nodes[self.getPath()[0]]['pos'].getX()
    #     yStart = graph.nodes[self.getPath()[0]]['pos'].getY()
    #     xEnd = graph.nodes[self.getPath()[1]]['pos'].getX()
    #     yEnd = graph.nodes[self.getPath()[1]]['pos'].getY()
    #
    #     dist = self.distanceFromSrcNode(graph)
    #
    #     if xStart == xEnd:  # if x=constant
    #         return Point(xStart, yStart + dist, 0)
    #
    #     m = (yStart - yEnd) / (xStart - xEnd)
    #     b = yStart - (m * xStart)  # y=Mx+b -> b=y-Mx
    #
    #     qa = (m ** 2) + 1
    #     qb = (2 * b * m) - (2 * m * yStart) - (2 * xStart)
    #     qc = (b * 2) - (2 * yStart * b) + (xStart * 2) - (dist ** 2)
    #
    #     x1, x2 = quadratic(qa, qb, qc)
    #     y1 = m * x1 + b
    #     y2 = m * x2 + b
    #     p1 = Point(x1, y1)
    #     p2 = Point(x2, y2)
    #     destP = graph.nodes[self.getPath()[1]]['pos']
    #     if self.passedPokPos.distance(p1) + p1.distance(destP) == self.passedPokPos.distance(destP):
    #         return p1
    #     else:
    #         return p2

    def _eq_(self, other):
        """for checking test of same Agents"""
        return self.id == other.id and self.value == other.value and self.dest == other.dest and self.src == other.src and self.speed == other.speed and self.pos == other.pos