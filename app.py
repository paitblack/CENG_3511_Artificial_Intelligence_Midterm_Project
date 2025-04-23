from flask import Flask, render_template, request, jsonify
import json
from dijkstra import dijkstra
from geopy.distance import geodesic
import time
from A_star_search import a_star_search

app = Flask(__name__)

with open("graph_mentese_custom.json") as f:
    graph = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

#  find_nearest_node() -> this function returns the node which is nearest to the node that user have chose.

def find_nearest_node(target_coord, coordinates):
    min_dist = float('inf')
    nearest_node = None
    
    for node, node_coord in coordinates.items():
        dist = geodesic(target_coord, node_coord).meters
        if dist < min_dist:
            min_dist = dist
            nearest_node = node
    
    return nearest_node

@app.route('/route', methods=['POST'])
def route():
    start_time = time.time()
    data = request.get_json()
    print("Gelen veri:", data)
    
    start_coord = tuple(data['start'])
    end_coord = tuple(data['end'])
    print("Baslangic:", start_coord)
    print("Bitis:", end_coord)

    coord_map = graph["coordinates"]
    print("Koordinatlar:", list(coord_map.items())[:3]) 

    start_node = find_nearest_node(start_coord, coord_map)
    end_node = find_nearest_node(end_coord, coord_map)
    print("Bulunan start:", start_node, "koo:", coord_map.get(start_node))
    print("Bulunan end:", end_node, "koo:", coord_map.get(end_node))

    if start_node == end_node:    #if start and end nodes' nearest node is the same return an error.
        print("HATA: ayni coordinatlar")
        return jsonify({"error": "cok yakin"}), 400

    try:
        astar_start = time.time()
        astar_path, astar_distance = a_star_search(graph, start_node, end_node)
        astar_time = (time.time() - astar_start) * 1000

        print("--------------------------------------------------------")
        print("A* Search Results:")
        print("Path Nodes:", astar_path)
        print("Distance:", astar_distance)
        print("Steps:", len(astar_path))
        print("Execution Time (ms):", astar_time)
        print("--------------------------------------------------------")

        dijkstra_time_start = time.time()
        path_nodes, distance = dijkstra(graph, start_node, end_node) 
        dijkstra_time_end = (time.time() - dijkstra_time_start) * 1000
        print("Dijkstra's Execution Time: ", dijkstra_time_end)
        
        print("Bulunan :", path_nodes)
        
        if not path_nodes:
            print("HATA: Bos yol")
            return jsonify({"error": "No path found"}), 400
            
        path_coords = [coord_map[node] for node in path_nodes]
        
        #interact with the frontend.
        return jsonify({
            "path": path_coords,
            "distance": distance,
            "steps": len(path_nodes),
            "path_nodes": path_nodes,
            "execution_time": (time.time() - start_time) * 1000,
            "start_node": start_node,
            "end_node": end_node
        })
    except Exception as e:
        print("Dijkstra hatasi:", str(e))
        return jsonify({"error": "Route calculation failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
