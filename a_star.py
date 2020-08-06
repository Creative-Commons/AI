from math import sqrt, inf
import pandas as pd


''' import data '''
map_json = {
    "Name":{"0":"Arad","1":"Bucharest","2":"Craiova","3":"Drobeta","4":"Eforie","5":"Fagaras","6":"Giurgiu","7":"Hirsova","8":"Iasi","9":"Lugoj","10":"Mehadia","11":"Neamt","12":"Oradea","13":"Pitesti","14":"Rimnicu Vilcea","15":"Sibiu","16":"Timisoara","17":"Urziceni","18":"Vaslui","19":"Zerind"},
    "X":{"0":62,"1":560,"2":319,"3":177,"4":824,"5":409,"6":518,"7":777,"8":680,"9":175,"10":182,"11":571,"12":121,"13":434,"14":290,"15":244,"16":67,"17":649,"18":735,"19":86},
    "Y":{"0":144,"1":409,"2":478,"3":463,"4":469,"5":217,"6":507,"7":378,"8":122,"9":333,"10":394,"11":73,"12":19,"13":353,"14":281,"15":202,"16":282,"17":376,"18":222,"19":83}}
distances_json = {
    "Place A":{"0":"Arad","1":"Arad","2":"Arad","3":"Bucharest","4":"Bucharest","5":"Craiova","6":"Craiova","7":"Drobeta","8":"Fagaras","9":"Hirsova","10":"Iasi","11":"Lugoj","12":"Mehadia","13":"Oradea","14":"Timisoara","15":"Pitesti","16":"Rimnicu Vilcea","17":"Sibiu","18":"Sibiu","19":"Urziceni","20":"Urziceni","21":"Vaslui","22":"Zerind","23":"Zerind","24":"Timisoara","25":"Sibiu","26":"Giurgiu","27":"Urziceni","28":"Rimnicu Vilcea","29":"Pitesti","30":"Craiova","31":"Bucharest","32":"Eforie","33":"Neamt","34":"Mehadia","35":"Drobeta","36":"Sibiu","37":"Lugoj","38":"Bucharest","39":"Pitesti","40":"Fagaras","41":"Rimnicu Vilcea","42":"Vaslui","43":"Hirsova","44":"Iasi","45":"Oradea"},
    "Place B":{"0":"Zerind","1":"Timisoara","2":"Sibiu","3":"Giurgiu","4":"Urziceni","5":"Rimnicu Vilcea","6":"Pitesti","7":"Craiova","8":"Bucharest","9":"Eforie","10":"Neamt","11":"Mehadia","12":"Drobeta","13":"Sibiu","14":"Lugoj","15":"Bucharest","16":"Pitesti","17":"Fagaras","18":"Rimnicu Vilcea","19":"Vaslui","20":"Hirsova","21":"Iasi","22":"Oradea","23":"Arad","24":"Arad","25":"Arad","26":"Bucharest","27":"Bucharest","28":"Craiova","29":"Craiova","30":"Drobeta","31":"Fagaras","32":"Hirsova","33":"Iasi","34":"Lugoj","35":"Mehadia","36":"Oradea","37":"Timisoara","38":"Pitesti","39":"Rimnicu Vilcea","40":"Sibiu","41":"Sibiu","42":"Urziceni","43":"Urziceni","44":"Vaslui","45":"Zerind"},
    "Distance":{"0":75,"1":118,"2":140,"3":90,"4":85,"5":146,"6":138,"7":120,"8":211,"9":86,"10":87,"11":70,"12":75,"13":151,"14":111,"15":101,"16":97,"17":99,"18":80,"19":142,"20":98,"21":92,"22":71,"23":75,"24":118,"25":140,"26":90,"27":85,"28":146,"29":138,"30":120,"31":211,"32":86,"33":87,"34":70,"35":75,"36":151,"37":111,"38":101,"39":97,"40":99,"41":80,"42":142,"43":98,"44":92,"45":71}}
cities = pd.DataFrame(map_json)
distances = pd.DataFrame(distances_json)


''' Table for storing calculated data '''
cities['g_n'] = inf
cities["h_n"] = inf
cities["f_n"] = inf
closed_list = []


''' g_n '''
def calculate_cost(source, node):
    if node['Place B'] == source['Name'].item():
        return 0
    else:
        ''' actual cost of edge '''
        cost = node["Distance"]

        previous = distances[distances['Place B'] == node['Place A']].min()
        return calculate_cost(source, previous) + cost


''' h_n '''
def calculate_heuristic(node, destination):
    current = cities[cities.Name == node['Place B']]
    heuristic = int(sqrt(
        (current.X.item() - destination.X.item()) ** 2 +
        (current.Y.item() - destination.Y.item()) ** 2
    ))
    return heuristic


def a_star(node, destination):
    node_name = node['Name'].item()
    print(node_name, "---->", end = " ")

    if node_name == destination['Name'].item():
        ''' node == destination '''
        print("Found")
        return True
    else:
        ''' find neighbour nodes '''
        neighbours = distances[distances['Place A'] == node_name]
        
        ''' calculate f_n for neighbour nodes '''
        for _,row in neighbours.iterrows():
            g_n = calculate_cost(node, row)
            h_n = calculate_heuristic(row, destination)

            ''' store values in table '''
            index = cities[cities.Name == row['Place B']].index
            cities.loc[index, 'g_n'] = g_n
            cities.loc[index, 'h_n'] = h_n
            cities.loc[index, 'f_n'] = g_n + h_n

        ''' choose minimum f_n, if valid '''
        cities.sort_values(by=['f_n'], inplace=True)
        index = 0
        while True:
            ''' select minimum f_n node '''
            selected = cities.iloc[index]
            ''' in closed list, or not neighbours '''
            if selected.Name in closed_list or neighbours[neighbours['Place B'] == selected.Name].empty:
                index += 1
            else:
                ''' add to closed list '''
                closed_list.append(selected.Name)
                break
    
        return a_star(cities[cities.Name == selected.Name], destination)


source_name = "Arad"
destination_name = "Neamt"
a_star(
    cities[cities.Name == source_name],
    cities[cities.Name == destination_name]
)