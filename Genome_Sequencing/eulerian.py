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

    start_found, end_found = False, False
    two_starts, two_ends = False, False
    start, end = '', ''
    proper_graph = []
    for key in set(edges_in.keys()).union(set(edges_out.keys())):
        equal = edges_in.get(key, 0) == edges_out.get(key, 0)
        proper_graph.append(equal)
        if not equal:
            if edges_in.get(key, 0) == 0:
                start = key
                if start_found:
                    # Multiple end nodes is bad, can't start at all of them
                    two_starts = True
                start_found = True
            if edges_out.get(key, 0) == 0:
                end = key
                if end_found:
                    # Multiple end nodes is bad, can't reach all of them
                    two_ends = True
                end_found = True

    if (not all(proper_graph)) and not (start_found and end_found and (not two_starts) and (not two_ends)):
        assert proper_graph is True, 'All nodes in the graph should have the same number of edges in as edges out, ' \
                                     'except the start and end node '

    if start_found and end_found:
        # Add a connection from the end of the graph to the beginning, to make the graph cyclic
        g[end] = [start]
        unused_edges.append((end, start))

    order = []
    seen_nodes = [list(g.keys())[0]]

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
        while next_node != starting_node or g.get(next_node, -1) == -1:
            seen_nodes.append(next_node)
            prev_node = next_node
            next_node = g[next_node].pop(0)
            order.insert(insert_position, (prev_node, next_node))
            unused_edges.remove((prev_node, next_node))

            # Update insert_position (But not if inserting at the end of the list)
            insert_position += (1 if insert_position > 0 else 0)
    order.insert(0, order[-1])

    if start_found and end_found:
        # Remove the last edge, as this connects the end of the graph to be the beginning
        return order[:-2]
    return order[:-1]


def main():
    directed_graph = {
        'TA': ['AA'],
        'AA': ['AT'],
        'AT': ['TG', 'TG', 'TG'],
        'TG': ['GC', 'GG', 'GT'],
        'GC': ['CC'],
        'CC': ['CA'],
        'CA': ['AT'],
        'GG': ['GG', 'GA'],
        'GA': ['AT'],
        'GT': ['TT'],
    }

    eulerian = find_eulerian(directed_graph)
    print(f'The Eulerian path for the given directed graph is:')
    print(' ⟶ '.join([f'({i}, {j})' for i, j in eulerian]))


if __name__ == '__main__':
    main()
