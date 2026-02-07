import heapq
import math
from .models import Node, Edge

WALKING_SPEED_KMPH = 5


# ---------- DISTANCE (Haversine) ----------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ---------- TIME ----------
def calculate_time(distance_km):
    return round((distance_km / WALKING_SPEED_KMPH) * 60, 2)  # minutes


# ---------- GRAPH ----------
def build_graph():
    graph = {}

    edges = Edge.objects.select_related("source", "destination")

    for edge in edges:
        src = edge.source.id
        dst = edge.destination.id

        if src not in graph:
            graph[src] = []

        graph[src].append((dst, edge.weight))

    return graph


# ---------- DIJKSTRA ----------
def dijkstra(start_name, end_name):
    nodes = {n.id: n for n in Node.objects.all()}

    start = Node.objects.get(name=start_name)
    end = Node.objects.get(name=end_name)

    graph = build_graph()

    pq = []
    heapq.heappush(pq, (0, start.id))

    distance_map = {start.id: 0}
    parent = {}

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current == end.id:
            break

        if current_dist > distance_map.get(current, float("inf")):
            continue

        for neighbor, weight in graph.get(current, []):
            new_dist = current_dist + weight

            if new_dist < distance_map.get(neighbor, float("inf")):
                distance_map[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))

    # ---------- PATH RECONSTRUCTION ----------
    path_ids = []
    cur = end.id

    while cur != start.id:
        path_ids.append(cur)
        cur = parent.get(cur)
        if cur is None:
            return [], 0, 0

    path_ids.append(start.id)
    path_ids.reverse()

    # ---------- OUTPUT ----------
    coords = []
    total_distance = 0

    for i in range(len(path_ids) - 1):
        n1 = nodes[path_ids[i]]
        n2 = nodes[path_ids[i + 1]]

        coords.append([float(n1.latitude), float(n1.longitude)])
        total_distance += haversine(
            n1.latitude, n1.longitude, n2.latitude, n2.longitude
        )

    last = nodes[path_ids[-1]]
    coords.append([float(last.latitude), float(last.longitude)])

    time = calculate_time(total_distance)

    return coords, round(total_distance, 3), time
