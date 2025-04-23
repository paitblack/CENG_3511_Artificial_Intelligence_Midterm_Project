import heapq
import math

def haversine_distance(coord1, coord2):

    # haversine_distance() -> haversine distance formula calculatest the distance between two coordinates.(in km)
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    #now we need to convert them to radians type.
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # formula implementation
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # radius of the earth.
    r = 6371
    return c * r

def a_star_search(graph, start_point, end_point):  # weight of the visited nodes(actual cost) + heuristics 
    nodes = graph["nodes"]
    edges = graph["edges"]
    coordinates = graph["coordinates"]
    
    g_cost = {node: float('inf') for node in nodes}
    g_cost[start_point] = 0
    
    f_cost = {node: float('inf') for node in nodes}
    f_cost[start_point] = haversine_distance(coordinates[start_point], coordinates[end_point])
    
    visited_nodes = {node: None for node in nodes}
    
    open_set = [(f_cost[start_point], start_point)]
    
    while open_set:
        current_f, current_node = heapq.heappop(open_set)
        
        if current_node == end_point:
            break
        
        for neighbor in edges.get(current_node, []):
            neighbor_node = neighbor["node"]
            neighbor_weight = neighbor["weight"]
            
            temp_g_cost = g_cost[current_node] + neighbor_weight
            
            if temp_g_cost < g_cost[neighbor_node]:
                visited_nodes[neighbor_node] = current_node
                g_cost[neighbor_node] = temp_g_cost
                h_cost = haversine_distance(coordinates[neighbor_node], coordinates[end_point])
                f_cost[neighbor_node] = temp_g_cost + h_cost
                heapq.heappush(open_set, (f_cost[neighbor_node], neighbor_node))
    
    path = []
    node = end_point
    while node:
        path.insert(0, node)
        node = visited_nodes[node]
    
    return path, g_cost[end_point]

graph_data = {
    "nodes": ["A", "B", "C", "D"],
    "edges": {
        "A": [{"node": "B", "weight": 2}, {"node": "C", "weight": 4}],
        "B": [{"node": "C", "weight": 1}, {"node": "D", "weight": 7}],
        "C": [{"node": "D", "weight": 3}],
        "D": []
    },
    "coordinates": {
        "A": [51.505, -0.09],
        "B": [51.51, -0.1],
        "C": [51.52, -0.12],
        "D": [51.515, -0.13]
    }
}

if __name__ == "__main__":
    print("----------A* Search Test----------")
    
    start_node = "A"
    end_node = "D"
    path, total_distance = a_star_search(graph=graph_data, start_point=start_node, end_point=end_node)
    
    print("Shortest path:", path)
    print("Total distance:", total_distance)
    
    print("Coordinates:")
    for node in path:
        coords = graph_data["coordinates"][node]
        print(f"{node}: {coords}")
    
    print("----------------------------------")