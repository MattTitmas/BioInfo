from typing import List, Dict
from queue import Queue

def find_eulerian(g: Dict[str, List[str]]):
    edges_in, edges_out = dict(), dict()
    unused_edges = []
    for key in g:
        edges_out[key] = len(g[key])
        for value in g[key]:
            unused_edges.append((key, value))
            edges_in[value] = edges_in.get(value, 0) + 1

    proper_graph = all([edges_in[key] == edges_out[key] for key in g])
    assert proper_graph is True, 'All nodes in the graph should have the same number of edges in as edges out'


    order = []
    seen_nodes = ['A']

    while len(unused_edges) > 0:
        starting_node, next_node = unused_edges.pop(0)
        if starting_node not in seen_nodes:
            unused_edges.append((starting_node, next_node))
            continue

        # Get position in  {order} in which to insert this sub loop
        insert_position = min([order.index(i) for i in order if i[1] == starting_node], default=-2) + 1
        order.insert(insert_position, (starting_node, next_node))

        # Update insert_position (But not if inserting at the end of the list)
        insert_position += (1 if insert_position > 0 else 0)
        while next_node != starting_node:
            seen_nodes.append(next_node)
            prev_node = next_node
            next_node = g[next_node].pop(0)
            order.insert(insert_position, (prev_node, next_node))
            unused_edges.remove((prev_node, next_node))

            # Update insert_position (But not if inserting at the end of the list)
            insert_position += (1 if insert_position > 0 else 0)
    return order


def main():
    directed_graph = {
        'A': ['B'],
        'B': ['C', 'F'],
        'C': ['D', 'F'],
        'D': ['A', 'G'],
        'E': ['C', 'D'],
        'F': ['E', 'H'],
        'G': ['E'],
        'H': ['B']
    }

    eulerian = find_eulerian(directed_graph)
    print(f'The Eulerian path for the given directed graph is:')
    print(' ⟶ '.join([f'({i}, {j})' for i, j in eulerian]))


if __name__ == '__main__':
    main()
