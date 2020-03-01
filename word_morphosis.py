import argparse

from _collections import defaultdict, deque


class PathNode:
    def __init__(self, val):
        self.val = val
        self.next = []


class Search:
    def __init__(self):
        self.shortest_path_length = float('inf')
        self.shortest_path = []
        self.paths = []
        self.visited_start = defaultdict(list) # store paths for the visited node
        self.visited_end = defaultdict(list)

    def update_path(self, path):
        self.paths.append(path)
        length = len(path)
        if length < self.shortest_path_length:
            self.shortest_path = path
            self.shortest_path_length = length

    def search(self, start, end, graph):
        '''
        Do a Bi-directional BFS to find all routes
        Todo: figure out how to not double count, for now paths stores all paths twice
        :param start: str
        :param end: str
        :param graph: dict
        :return:
        '''
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
    args = parser.parse_args()

    from fetch_data import FetchData
    data = FetchData(test=args.test)

    search_component = Search()
    search_component.search(args.start_word, args.end_word, data.graph)
    
    print(f'Shortest path length: {search_component.shortest_path_length}')
    print(f'Shortest path: {search_component.shortest_path}')
    print(f'Number of paths found: {len(search_component.paths)//2}')
