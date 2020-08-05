import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from math import sqrt
import pandas as pd


cities = pd.read_csv("map.csv")
distances = pd.read_csv("distances.csv")


class Graph:
    def __init__(self):
        self.costs = []
        self.g_n_list = {}
        self.h_n_list = {}
        

    def calculate_cost(self, source, node):
        if node == source:
            return 0
        else:
            if node in self.g_n_list:
                return self.g_n_list[node]
            else:
                edge = distances[distances['Place B'] == node].iloc[0]

                if edge.empty:
                    return 0
                x = self.calculate_cost(source, str(edge['Place A'])) + int(edge.Distance)
                self.g_n_list[node] = x
                return x

    def calculate_heuristic(self, node, destination):
        ''' euclidean distance '''
        if node in self.h_n_list:
            return self.h_n_list[node]
        else:
            node_coords = cities[cities.Name == node]
            destination_coords = cities[cities.Name == destination]
            x = sqrt(
                (int(node_coords.X) - int(destination_coords.X)) ** 2 +
                (int(node_coords.Y) - int(destination_coords.Y)) ** 2
            )
            self.h_n_list[node] = x
            return x


    def a_star(self, current, destination, visited_nodes):
        if current == destination:
            print('found')
            return True
        available_nodes = distances[distances['Place A'] == current]

        f_n_list = []

        ''' f_n = g_n + h_n
            - g_n = cost
            - h_n = heuristic '''

        for _, row in available_nodes.iterrows():
            name = str(row['Place B'])
            
            g_n = self.calculate_cost(current, name)
            h_n = self.calculate_heuristic(name, destination)
            f_n_list.append(g_n + h_n)

            visited_nodes.append(name)

        pos = f_n_list.index(min(f_n_list))     #select minimum f(n)
        selection = available_nodes.iloc[pos]
        print(selection['Place B'])
        #print(self.h_n_list)

        return self.a_star(str(selection['Place B']), destination, visited_nodes)



    def a_starter(self, source, destination):
        #print(source, destination)
        self.a_star(source, destination, [])


G = Graph()
G.a_starter("Arad", "Vaslui")

#G.a_starter("Arad", "Neamt")
# Reaching Neamt seems to be a problem rn, help.


''' IGNORE BELOW '''
'''
    def create_animation(self):
        self.ax.scatter([cities['X']], [cities['Y']], color="black")
        for _, row in cities.iterrows():    
            self.ax.annotate(
                row['Name'], (row['X'], row['Y']),
                textcoords="offset points",
                xytext=(0,5),
                ha='center'
            )
        return self.ax,

    def animate_step(self, i):
        for index, row in distances.iterrows():
            A = cities[cities.Name == row['Place A']]
            B = cities[cities.Name == row['Place B']]
            self.ax.plot([A.X, B.X], [A.Y, B.Y], color="#002040")
        for line in self.selected:
            self.ax.plot(line[0], line[1], color="#002040")
        return self.ax,
    
    def start_animation(self):  
        plt.gca().invert_yaxis()
        self.anim = animation.FuncAnimation(
            self.fig, self.animate_step,
            frames=20,
            init_func=self.create_animation,
            interval = delay, blit=True, 
        )

'''