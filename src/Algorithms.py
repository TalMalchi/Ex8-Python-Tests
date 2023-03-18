import random

from src.Pokemon import Pokemon
from src.client import Client
from timeStampsDemo import *


def assignAgentSrcNodes(numOfAgents: int, client: Client, pokLst: list, graph: nx.DiGraph) -> int:
    """Function to assign the agents their initial positions. returns the number of agents which have a pokemon to
    currently go to (if there are more agents than pokemons, not all agents might have a destination"""

    if numOfAgents == len(pokLst):
        # if the amount of agents is equals to the pokemon amount, we will put each agent next to each pokemon
        for i in range(numOfAgents):
            client.add_agent("{\"id\":" + str(pokLst[i].node_src) + "}")
        return numOfAgents
    elif numOfAgents < len(pokLst):  # else, we will put the agent next to the pokemon with the highest value
        for i in range(numOfAgents):
            client.add_agent("{\"id\":" + str(pokLst[i].node_src) + "}")
        return numOfAgents
    else:  # numOfAgents > len(pokLst) - else, we will set random position to each agent
        for i in range(len(pokLst)):
            client.add_agent("{\"id\":" + str(pokLst[i].node_src) + "}")
        for i in range(numOfAgents - len(pokLst)):
            random.seed(a=0)
            rand = random.randint(len(graph))
            while rand not in graph.nodes:
                rand = random.randint(len(graph))
            client.add_agent("{\"id\":" + str(rand) + "}")
        return len(pokLst)


def tsp(graph: nx.DiGraph, srcNodesToVisit: list, pokLst: list):
    """Calculates the shortest path between a list of nodes, given the graph. Does not calculate the time needed to
    traverse (it is also dependent on speed of agent."""
    copyNodesToVisit = srcNodesToVisit.copy()  # copy the original list so that it remains unchanged
    shortestPathDist = sys.maxsize  # init the shortest path distance variable to max size possible
    totalDist = 0
    totalShortestPath = []
    minIndex = 0
    while len(copyNodesToVisit) != 1:
        for j in range(1, len(copyNodesToVisit)):
            if len(totalShortestPath) == 0:  # if there is just one edge in the path, we will set it to the CurrminLen
                currMinLength = nx.shortest_path_length(graph, source=copyNodesToVisit[0], target=copyNodesToVisit[j])
            else:  # else , we will check the shortestPath between every two nodes, and will update the minCurrLen everytime
                currMinLength = nx.shortest_path_length(graph, source=totalShortestPath[-1], target=copyNodesToVisit[j])
            if currMinLength < shortestPathDist:
                shortestPathDist = currMinLength
                minIndex = j
        try:
            currMinPath = nx.shortest_path(graph, source=copyNodesToVisit[0], target=copyNodesToVisit[minIndex])  # set the minPath with the minIndex that gives the currMinLength
            for node in currMinPath:  # add each node in the CurrMinPath to totalShortestPath
                totalShortestPath.append(node)
            if minIndex >= 1:
                totalShortestPath.append(pokLst[minIndex - 1].get_node_dest())
                totalDist += shortestPathDist + graph.get_edge_data(pokLst[minIndex - 1].get_node_src(), pokLst[minIndex - 1].get_node_dest())['weight']
        except:
            pass
        copyNodesToVisit.pop(0)
    return totalDist, totalShortestPath


def sortPokLst(graph: nx.DiGraph, agent: Agent, oldPokLst: list):
    """"sort the PokLst according to Agent's path"""
    agentPath = agent.getPath()
    newPokLst = []
    for i in range(len(agentPath) - 1):  # go all over agent's path and sort according to src and dest
        currSrc = agentPath[i]
        currDest = agentPath[i + 1]
        for pok in oldPokLst:
            if currSrc == pok.get_node_src() and currDest == pok.get_node_dest():
                newPokLst.append(pok)
                oldPokLst.remove(pok)
    return newPokLst


def assignNewPokemonToAgent(graph: nx.DiGraph, agentLst: list, pokemon: Pokemon):  # , timeStamps: list):
    """Chooses the best agent to allocate the new pokemon to, using TSP. Returns the ID of the agent which was chosen
    for the new pokemon"""
    minDist = sys.maxsize
    minPath = []
    minPokLst = []
    minAgentId = 0
    for i in range(len(agentLst)):
        # pokemon list of agent, if it were to be permanently added to it (to be verified)
        tempPokLst = agentLst[i].getPokLst()
        tempPokLst.append(pokemon)

        # Source nodes of all pokemons to be hypothetically passed
        if agentLst[i].getDest() != -1:
            srcNodeListToPass = [agentLst[i].getDest()]
        for pok in tempPokLst:
            srcNodeListToPass.append(pok.get_node_src())

        # check the sortestPath for each agent on the same pokemonLst
        tempShortDist, tempShortPath = tsp(graph, srcNodeListToPass, tempPokLst)
        if tempShortDist < minDist:  # update the minDist each time
            minDist = tempShortDist
            minPath = tempShortPath
            minAgentId = agentLst[i].getId()
            minPokLst = tempPokLst
    minPath.insert(0, agentLst[minAgentId].getSrc())
    agentLst[minAgentId].setPath(minPath)
    sortedPokLst = sortPokLst(graph, agentLst[minAgentId], minPokLst)  # return the shortestPath
    agentLst[minAgentId].setPokLst(sortedPokLst)  # up

    # pokIndex = 0
    # for i in range(len(minPath) - 1):
    #     if sortedPokLst[0].get_node_src() == minPath[i] and sortedPokLst[0].get_node_dest() == minPath[i + 1]:
    #         pokIndex = i
    #         break

    # timeStamps = pokemonTimeStamps(timeStamps, graph, agentLst[minAgentId], pokIndex)
    return agentLst  # , timeStamps