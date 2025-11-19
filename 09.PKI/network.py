from certificate import Certificate
from collections import deque

def build_chain(start_node, end_node, trust_graph):
    """
    :param start_node: nu start otsuda
    :param end_node: nu eto izhem
    :param trust_graph: graph kotoryi svyaznyi

    :return: chain
    """

    if start_node == end_node:
        return [start_node]
    
    parent = {}
    visited = set()
    queue = deque()

    queue.append(start_node)
    visited.add(start_node)
    parent[start_node] = None


    # BFS
    while queue:
        current_node = queue.popleft()

        for neighbor in trust_graph.get(current_node, []):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current_node

                if neighbor == end_node:
                    path = []
                    node = end_node
                    while node is not None:
                        path.append(node)
                        node = parent.get(node)
                    return path[::-1]

    return None

def main():
    print("Сетевая PKI")

    trust_graph_network = {
        "a": ["b", "c"],
        "b": ["a", "x", "c"],
        "c": ["a", "d", "y", "b"],
        "d": ["c", "z"],
        "x": ["b"],
        "y": ["c"],
        "z": ["d"]
    }
    
    print("graph doveriya")
    for node, neighbours in trust_graph_network.items():
        print(f"{node} -> {neighbours}")
        
    initial = "a"
    print(f"chain from {initial} to z")

    chain = build_chain("z", initial, trust_graph_network)
    if chain:
        print(" -> ".join(chain))
    else:
        print("chain not found")

    print("path to nonexistence")

    chain = build_chain(initial, "abracadabra", trust_graph_network)
    if chain:
        for node in chain:
            print(node)
    else:
        print("chain not found")


if __name__ == "__main__":
    main()