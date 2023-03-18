import sys

import networkx as nx

from src.Agent import Agent


def initialTimeStamps(timestamps: list, graph: nx.DiGraph, agent: Agent, toAdd: float = 0) -> list:
    pokSrc = agent.getPokLst()[0].get_node_src() # Extract the source of the pokémon (means the node id of the start of the edge)
    pokDest = agent.getPokLst()[0].get_node_dest()  # Extract the destination of the pokémon (means the node id of the end of the edge)
    wholeEdgeLength = graph.nodes[pokSrc]['pos'].distance(graph.nodes[pokDest]['pos'])  # compute the length of the whole edge the pokémon is located on
    srcToPokLength = graph.nodes[agent.getPokLst()[0].get_node_src()]['pos'].distance(agent.getPokLst()[0].getPos())  # Compute the distance from the source of the edge the pokemon locate on, to the pokemon
    percentageOfEdge = srcToPokLength / wholeEdgeLength  # Find the precentage of the length of the edge that the pokémon locate at(fro src to pokemon) from the whole edge.
    timeSrcToPok = percentageOfEdge * (graph.get_edge_data(pokSrc, pokDest)['weight'] / agent.get_speed())
    timestamps.append((toAdd + timeSrcToPok, agent.getId()))  # Add the time we computed to timestamps list
    sorted(timestamps, key=lambda x: x[0])  # Sort the timestemps list by the first element of tuple
    return timestamps


def pokemonTimeStamps(timestamps: list, graph: nx.DiGraph, agent: Agent, idPokDestNode: int) -> list:
    """function add the timeStamps when the agent visit the closest pokemon.
    Right now, we are at a POKEMON (at the middle of an edge)"""
    pokLst = agent.getPokLst()  # save the pok list of the agent
    duplPokExists = False  # Attribute for checking if there is another pokémon on the same edge
    minDuplPokemon = sys.maxsize
    for i in range(1, len(pokLst)):
        # We will check if the current pokémon has the same src and dest as another pokémon
        if pokLst[i].get_node_src() == pokLst[0].get_node_src() and pokLst[i].get_node_dest() == pokLst[0].get_node_dest():
            # If src and dest of the pokémon are the same than we will update duplPokExists
            duplPokExists = True
            # In case we have more than 2 pokemons on the same edge, we will check which one is the closest to the current pokemon
            if pokLst[i].getPos().distance(pokLst[0].getPos()) < pokLst[minDuplPokemon].getPos().distance(pokLst[0].getPos()):
                minDuplPokemon = i

    agentPath = agent.getPath()[:idPokDestNode]
    wholeEdgeLength = graph.nodes[agentPath[0]]['pos'].distance(graph.nodes[agentPath[1]]['pos'])

    if duplPokExists:  # If there are few pokemons on the same edge
        currToDestLength = agent.getPos().distance(pokLst[minDuplPokemon].getPos())  # We will compute the distance between the agent to the closest pokemon
    else:  # If there is only one pokemon on the current edge
        currToDestLength = agent.getPos().distance(graph.nodes[agentPath[1]]['pos'])  # We will compute the distance between the agent to the end of the edge
    percentageOfEdge = currToDestLength / wholeEdgeLength  # Find the precentage of the length from agent to next pokemon or from agent to dest node from the whole edge.
    timePokToDest = percentageOfEdge * (graph.get_edge_data(agentPath[0], agentPath[1])['weight'] / agent.get_speed())
    timestamps.append((timePokToDest, agent.getId()))  # Add the time we computed to timestamps list
    # Got to path[1]. Need to get to next nodes + pokemon

    for nodeId in range(1, len(agentPath) - 2):
        currEdgeWeight = graph.get_edge_data(agentPath[nodeId], agentPath[nodeId + 1])['weight']
        timeToNextNode = currEdgeWeight / agent.speed
        timestamps.append((timestamps[-1][0] + timeToNextNode, agent.getId()))

    timestamps = initialTimeStamps(timestamps, graph, agent, toAdd=timestamps[-1][0])
    return timestamps
