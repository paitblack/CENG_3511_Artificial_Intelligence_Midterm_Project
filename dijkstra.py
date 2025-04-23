import heapq

def dijkstra(graph, start_point, end_point):

    nodes = graph["nodes"]                                        # ["A", "B", "C", "D"]
    edges = graph["edges"]                                        # "A": [{"node": "B", "weight": 2}, {"node": "C", "weight": 4}],......

    distBetwNodes = {node : float("inf") for node in nodes}       #set the all distances as inf as a new dictionary.
    distBetwNodes[start_point] = 0

    # aim : check all the edges than choose the less weight, add to path(node) and distance(weight).

    visitedNodes = {node: None for node in nodes}

    queue = [(0, start_point)]

    while queue:

        currentDistance, currentN  = heapq.heappop(queue)

        if currentN == end_point:
            break
        
        for neighbor in edges.get(currentN, []):
            nextN = neighbor["node"]
            weightN = neighbor["weight"]
            newDistance = currentDistance + weightN

            if newDistance < distBetwNodes[nextN]:              #if less than - add to previous than do the calculations..
                distBetwNodes[nextN] = newDistance
                visitedNodes[nextN] = currentN
                heapq.heappush(queue, (newDistance, nextN))
    
    path = []
    node = end_point
    while node:
        path.insert(0, node)
        node = visitedNodes[node]

    return path, distBetwNodes[end_point]

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

    print("----------TEST----------")

    start_node = "A"
    end_node = "D"
    path, total_distance = dijkstra(graph = graph_data, start_point = start_node, end_point = end_node)

    print("Shortest path: ", path)
    print("Total distance: ", total_distance)

    print("Coordinates: ")
    for node in path:
        coords = graph_data["coordinates"][node]
        print(f"{node}: {coords}")

    print("------------------------")