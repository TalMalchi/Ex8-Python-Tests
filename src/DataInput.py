import json

import networkx as nx

from src.Agent import Agent
from src.Point import Point
from src.Pokemon import Pokemon


def loadGraph(stringGraph):  #have test
    """load the graph- Nodes and Edges into graph object """
    jsonGraph = json.loads(stringGraph)
    graph = nx.DiGraph()
    for node in jsonGraph["Nodes"]:
        graph.add_node(int(node["id"]), pos=Point(string=node["pos"]))

    for edge in jsonGraph["Edges"]:
        graph.add_edge(int(edge["src"]), int(edge["dest"]), weight=float(edge["w"]))

    return graph


def loadAllPokemons(pokemons, graph: nx.DiGraph): #have test
    """loads all the pokemons into pokemon object"""
    pokLst = []
    jsonTemp = json.loads(pokemons)
    for i in range(len(jsonTemp['Pokemons'])):
        pokLst.append(Pokemon(graph, jsonStr=jsonTemp['Pokemons'][i]))
    pokLst.sort(key=lambda x: x.getValue(), reverse=True)
    return pokLst


def appendToAllPokemons(pokemons, graph: nx.DiGraph, pokLst: list):
    tempLst = loadAllPokemons(pokemons, graph)
    for i in pokLst:
        if i in tempLst:
            tempLst.remove(i)
    for i in tempLst:
        pokLst.append(i)
    pokLst.pop(0)
    return pokLst

# def appendToAllPokemons(pokemons, graph: nx.DiGraph, pokLst: list):#TODO test
#     """Check if pokemon exists in the list of pokemons. Add it if it does not. As the position of the pokemon is
#     immutable, the comparison is performed on it"""
#     jsonTemp = json.loads(pokemons)
#     for i in range(len(jsonTemp['Pokemons'])):
#         if len(pokLst) >= 1:
#             if jsonTemp['Pokemons'][i]['Pokemon']['pos'] != pokLst[i].getPosString():
#                 pokAdded = Pokemon(graph, jsonStr=jsonTemp['Pokemons'][i])
#                 pokLst.append(pokAdded)
#         else:
#             pokAdded = Pokemon(graph, jsonStr=jsonTemp['Pokemons'][i])
#             pokLst.append(pokAdded)
#     pokLst.pop(0)
#     pokLst.sort(key=lambda x: x.getValue(), reverse=True)
#     return pokLst


def loadAllAgents(agents): #have test
    """ loads all the pokemons into agent """
    agentLst = []
    jsonTemp = json.loads(agents)
    for i in range(len(jsonTemp['Agents'])):
        agentLst.append(Agent(jsonStr=jsonTemp['Agents'][i]['Agent']))
    return agentLst


# def addAllTimeStamps(agentLst: list, graph: nx.DiGraph, startTime): #TODO test (they said never used)
#     """add all timestemps of each agent to one list"""
#     timestamps = []
#     for agent in agentLst:
#         timestamps.append(agent.addTimeStamps(graph, timestamps, agent.getPath(), startTime))
#     return timestamps

