import argparse

from _collections import defaultdict, deque


class PathNode:
    def __init__(self, val):
        self.val = val
        self.next = []


class Search:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.shortest_path_length = float('inf')
        self.shortest_path = []
        self.paths = defaultdict(set)
        self.visited_start = defaultdict(list) # store paths for the visited node
        self.visited_end = defaultdict(list)

    def read_paths(self, start=None, path=None):
        if path is None:
            path = []

        if start is None:
            start = self.start

        path.append(start)
        for child in self.paths[start]:
            if child != self.end:
                yield from self.read_paths(child, path)
            else:
                yield path + [self.end]

    @property
    def total_paths_length(self):
        return len(list(_ for _ in self.read_paths()))

    def update_path(self, path):
        curr = path[0]
        for node in path[1:]:
            if node not in self.paths[curr]:
                self.paths[curr].add(node)
            curr = node

        length = len(path)
        if length < self.shortest_path_length:
            self.shortest_path = path
            self.shortest_path_length = length

    def search(self, graph, start=None, end=None):
        '''
        Do a Bi-directional BFS to find all routes
        Todo: figure out how to not double count, for now paths stores all paths twice
        :param start: str
        :param end: str
        :param graph: dict
        :return:
        '''
        if start is None:
            start = self.start

        if end is None:
            end = self.end

        self.visited_start[start].append(start)
        self.visited_end[end].append(end)

        q_start = deque([start])
        q_end = deque([end])

        while q_start and q_end:
            x, y = q_start.popleft(), q_end.popleft()
            for one_hop in graph[x]:
                if one_hop in self.visited_end:
                    # check if it exists in other
                    path = self.visited_start[x] + self.visited_end[one_hop]
                    self.update_path(path)
                elif one_hop not in self.visited_start:
                    q_start.append(one_hop)
                    self.visited_start[one_hop] += self.visited_start[x] + [one_hop]

            for one_hop in graph[y]:
                if one_hop in self.visited_start:
                    # check if it exists in other
                    path = self.visited_start[one_hop] + self.visited_end[y]
                    self.update_path(path)
                elif one_hop not in self.visited_end:
                    q_end.append(one_hop)
                    self.visited_end[one_hop] += [one_hop] + self.visited_end[y]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("start_word", help="Start word to search from")
    parser.add_argument("end_word", help="End word to search till")
    parser.add_argument("--test", help="run on test data",
                        action="store_true")
    parser.add_argument("--show_paths", help="Show all the paths",
                        action="store_true")
    args = parser.parse_args()

    from fetch_data import FetchData
    data = FetchData(test=args.test)

    search_component = Search(args.start_word, args.end_word)
    search_component.search(data.graph)
    
    print(f'Shortest path length: {search_component.shortest_path_length}')
    print(f'Shortest path: {search_component.shortest_path}')
    print(f'Number of paths found: {search_component.total_paths_length}')

    if args.show_paths:
        print('Printing all the paths')
        for path in search_component.read_paths():
            print(path)
