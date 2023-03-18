import sys

import pygame as pg
from pygame.locals import *

# from GUI.InputField import InputField
from GUI.Button import Button
from src.Agent import *
from src.Point import *


def init(g: nx.DiGraph()):
    """Initializing GUI to be called from outside the class"""
    gui = GUI(g)
    gui.init_gui()
    return gui


def checkMinMax(graph: nx.DiGraph()):  # graph: nx.DiGraph()):
    # static variables, for GUI
    min_value = {'x': -sys.maxsize, 'y': -sys.maxsize, 'z': 0}
    max_value = {'x': sys.maxsize, 'y': sys.maxsize, 'z': 0}
    for i in graph.nodes():
        # define min max values to present the graph
        if min_value['x'] < graph.nodes()[i]['pos'].getX():
            min_value['x'] = graph.nodes()[i]['pos'].getX()
        if min_value['y'] < graph.nodes()[i]['pos'].getY():
            min_value['y'] = graph.nodes()[i]['pos'].getY()

        if max_value['x'] > graph.nodes()[i]['pos'].getX():
            max_value['x'] = graph.nodes()[i]['pos'].getX()
        if max_value['y'] > graph.nodes()[i]['pos'].getY():
            max_value['y'] = graph.nodes()[i]['pos'].getY()

    return min_value, max_value


def get_away_from_edge_of_screen(x, y, screen_x_size, screen_y_size):
    """If a point is too close to one of the edges of the screen, we transfer the values slightly further from the edge,
     so that a value can be presented in a visually pleasant way"""
    if y < 5:
        y += 15
        x += 15
    if x > screen_x_size - 5:
        x -= 15
        y -= 15
    if y > screen_y_size - 5:
        y -= 15
        x += 15
    return x, y


class GUI:
    circle_rad = 5  # a constant radius of most of the nodes

    def __init__(self, gr: nx.DiGraph()):
        """Basic constructor"""
        self.screen_y_size = None
        self.screen_x_size = None
        self.screen = None
        self.button_stop = None
        self.graph = gr

    def normalize_x(self, currNodeVal) -> float:
        """Normalize the x value according to the current size of the screen"""
        result = checkMinMax(self.graph)
        return (currNodeVal - result[0]['x']) / (result[1]['x'] - result[0]['x']) * (self.screen_x_size - 20) + 10

    def normalize_y(self, currNodeVal) -> float:
        """Normalize the y value according to the current size of the screen"""
        result = checkMinMax(self.graph)
        return (currNodeVal - result[0]['y']) / (
                result[1]['y'] - result[0]['y']) * (self.screen_y_size - 20) + 10

    def drawArrowForEdge(self, src_node_x, src_node_y, dest_node_x, dest_node_y, colour):
        """Function to draw an arrowhead in the direction of the line
        adapted from https://stackoverflow.com/questions/43527894/drawing-arrowheads-which-follow-the-direction-of-the-line-in-pygame/43529178"""
        start = (src_node_x, src_node_y)
        end = (dest_node_x, dest_node_y)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pg.draw.polygon(self.screen, colour, (  # drawing a rectangle to represent the arrowhead
            (end[0] + 5 * math.sin(math.radians(rotation)), end[1] + 5 * math.cos(math.radians(rotation))),
            (end[0] + 5 * math.sin(math.radians(rotation - 120)), end[1] + 5 * math.cos(math.radians(rotation - 120))),
            (end[0] + 5 * math.sin(math.radians(rotation + 120)), end[1] + 5 * math.cos(math.radians(rotation + 120)))))

    def display_temp_text(self, text: str, pos: [int, int]):
        """Display a text received, at a given position (x,y). The text shall always be black, on white background
        (can easily be adapted to any other values). The function returns a timestamp of the time when the text was
        displayed"""
        font = pg.font.SysFont('Arial', 15)
        text_out = font.render(text, True, (0, 0, 0), (255, 255, 255))  # font used
        textRect = text_out.get_rect()  # creating frame box for the text
        textRect.bottomleft = pos  # bottom left corner of the text box
        self.screen.blit(text_out, textRect)  # print to screen
        pg.display.update()  # update the window
        return pg.time.get_ticks()  # start time

    def draw_graph_nodes(self):
        """Plot the nodes of the graph, using normalization mentioned above. """
        for node in self.graph.nodes():
            x = self.graph.nodes()[node]['pos'].getX()
            y = self.graph.nodes()[node]['pos'].getY()

            # Normalizing values to be between the size of the canvas
            x = self.normalize_x(x)
            y = self.normalize_y(y)

            pg.draw.circle(self.screen, (0, 0, 0), (x, y), GUI.circle_rad)  # drawing the nodes themselves

            # printing the id of the node beside it on the graph
            y -= 15
            x, y = get_away_from_edge_of_screen(x, y, self.screen_x_size, self.screen_y_size)
            font = pg.font.SysFont('Arial', 20)
            text = font.render(str(node), True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            self.screen.blit(text, text_rect)

    def draw_one_node(self, radius: int, colour: Color, center_point: Point):
        """function drawing circle """
        pg.draw.circle(self.screen, colour, center_point, radius)  # colour is color, center_point is center, radius is radius.

    def drawPoks(self, pokLst: list, radius: float):
        """function draw pokemons (as circ- if negative value, it will be draw in red if positive value, it will be draw in blue"""
        for pok in pokLst:
            norm_x = self.normalize_x(pok.getPos().getX())
            norm_y = self.normalize_y(pok.getPos().getY())
            if pok.getType() > 0:  # If the value is positive
                # self.normalize_x(src_node_x)
                pg.draw.circle(self.screen, (0, 0, 255), (norm_x, norm_y), radius) # colour is blue, center_point is center, radius is radius.
            else:
                pg.draw.circle(self.screen, (255, 0, 0), (norm_x, norm_y), radius) # colour is red, center_point is center, radius is radius.

    def drawAgents(self, agentLst: list, radius: float):
        """function draw agents"""
        for agent in agentLst:
            norm_x=self.normalize_x(agent.getPos().getX())
            norm_y=self.normalize_y(agent.getPos().getY())
            pg.draw.circle(self.screen, (0, 255, 0), (norm_x, norm_y), radius)  # colour is green, center_point is center, radius is radius.

    def draw_one_edge(self, edgeSrcID, edgeDestID, colour):
        """Function to plot a single edge according to all the data received by the function."""
        # Setting variables for readability and for effectiveness of the code

        pos_src = self.graph.nodes[edgeSrcID]['pos']
        src_node_x = pos_src.x
        src_node_y = pos_src.y

        pos_dest = self.graph.nodes[edgeDestID]['pos']
        dest_node_x = pos_dest.x
        dest_node_y = pos_dest.y

        # Normailizing
        src_node_x = self.normalize_x(src_node_x)
        src_node_y = self.normalize_y(src_node_y)
        dest_node_x = self.normalize_x(dest_node_x)
        dest_node_y = self.normalize_y(dest_node_y)

        # Below we find the point on the edge that ends at the circles' circumference, so that the arrow does not
        # seem "inside" the node
        m = (dest_node_y - src_node_y) / (dest_node_x - src_node_x)  # m in the linear function y = mx + b
        b = dest_node_y - (m * dest_node_x)  # b in the linear function y = mx + b

        # After calculations, the needed values to be passed to the quadratic equations
        a1 = ((m ** 2) + 1)
        b1 = ((-2) * dest_node_x - (2 * dest_node_y * m) + (2 * m * b))
        c1 = ((dest_node_x ** 2) + (dest_node_y ** 2) - (2 * b * dest_node_y) + (b ** 2) - (
                (GUI.circle_rad + 5) ** 2))
        x1, x2 = quadratic(a1, b1, c1)

        # Correlating y values to each of the x values
        y1 = (m * x1) + b
        y2 = (m * x2) + b
        point1 = Point(x1, y1, 0)
        point2 = Point(x2, y2, 0)

        # Finding the wanted node out of the 2 received
        # Point(src_node_x, src_node_y, 0).distance(Point(point1[0], point1[1], 0))
        if Point(src_node_x, src_node_y, 0).distance(point1) < Point(src_node_x, src_node_y, 0).distance(point2):
            # if distance([src_node_x, src_node_y], point1) < distance([src_node_x, src_node_y,0], point2):
            dest_node_x = point1.getX()
            dest_node_y = point1.getY()
        else:
            dest_node_x = point2.getX()
            dest_node_y = point2.getY()

        # Drawing the line of the arrow
        pg.draw.line(self.screen, colour, (src_node_x, src_node_y), (dest_node_x, dest_node_y), 2)
        # Drawing the arrowhead
        self.drawArrowForEdge(src_node_x, src_node_y, dest_node_x, dest_node_y, colour)

    def draw_graph_edges(self):
        """Function to iterate and plot all edges of the graph """
        # for edgeSrcID in self.graph.edges:
        #     try:
        #         for edgeDestID in self.graph.edges
        #             self.draw_one_edge(screen, screen_x_size, screen_y_size, edgeSrcID, edgeDestID, (0, 0, 0))
        #     except:
        #         continue
        for edgeSrcID in self.graph.edges:
            try:
                for edgeDestID in self.graph.edges:
                    self.draw_one_edge(edgeSrcID, edgeDestID, (0, 0, 0))
            except:
                continue


        for edgeSrcID in self.graph.edges:
            # curr = self.graph.edges(edgeSrcID)
            self.draw_one_edge(edgeSrcID[0], edgeSrcID[1], (0, 0, 0))

            #   dist_pokemon_src = graph.nodes[pok.get_node_src()]['pos']
            # for edgeDestID in self.graph.out_edges(edgeSrcID.dataG.edges.data("weight", default=1)):

        # def draw_graph_edges(self, screen, screen_x_size, screen_y_size):
        #     """Function to iterate and plot all edges of the graph """
        #     for edgeSrcID in self.graph.get_graph().get_all_v().keys():
        #         try:
        #             for edgeDestID in self.graph.get_graph().all_out_edges_of_node(edgeSrcID).keys():
        #                 self.draw_one_edge(screen, screen_x_size, screen_y_size, edgeSrcID, edgeDestID, (0, 0, 0))
        #         except:
        #             continue

    def redraw(self, pokLst: list = [], agentLst: list = []):  ######dont sure we need it
        """After a change has been made, a method to replot the graph and the buttons"""
        self.screen.fill((255, 255, 255))  # white background
        self.screen_x_size = self.screen_x_size
        self.screen_y_size = self.screen_y_size
        self.draw_graph_edges()
        self.draw_graph_nodes()
        if len(pokLst) != 0:
            self.drawPoks(pokLst, 6)
        if len(agentLst) != 0:
            self.drawAgents(agentLst, 9)

        # Button
        self.button_stop.show(self.screen)
        # pg.display.update()

    ###############################################################################################
    def init_gui(self):
        pg.init()
        pg.display.set_caption('Pokémon Game')
        self.screen_x_size = 800  # Default size of the window
        self.screen_y_size = 600
        self.screen = pg.display.set_mode((self.screen_x_size, self.screen_y_size), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.screen.fill((255, 255, 255))  # white background

        # Initializing button
        self.button_stop = Button("Stop Game", (0, 0))
        self.redraw()
        pg.display.update()

    def guiHandle(self, running, pokLst: list, agentLst: list, jsonStr: str, time_to_end):
        for event in pg.event.get():  # for each event
            if event.type == pg.QUIT or self.button_stop.click(event):  # user closed window
                running = False
                break
            elif event.type == VIDEORESIZE:  # If the window was resized
                self.screen_x_size = pg.display.Info().current_w
                self.screen_y_size = pg.display.Info().current_h
        self.redraw(pokLst, agentLst)
        overallPoint = "Overall points earned by agents: " + str(jsonStr['grade'])
        moveCount = "Total moves performed: " + str(jsonStr['moves'])
        timeRemaining = "Time remaining: " + time_to_end
        self.display_temp_text(overallPoint, [5, self.button_stop.size[1] + 25])
        self.display_temp_text(moveCount, [5, self.button_stop.size[1] + 40])
        self.display_temp_text(timeRemaining, [5, self.button_stop.size[1] + 55])

        pg.display.update()
        return running
