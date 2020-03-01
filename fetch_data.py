import requests
import argparse

from _collections import defaultdict

from test_data import t_data


class FetchData:
    uri = 'https://www.bestwordlist.com/5letterwords.txt'

    def __init__(self, test=False):
        self.test = test
        self.graph = defaultdict(set)
        self.all_words = set()
        self.fetch_and_create_graph()

    def fetch_and_create_graph(self):
        '''
        Get data using requests

        For each word in the response, create and add them to `buckets`
            WELSH goes into W_LSH, WE_SH, WEL_H and WELS_ buckets
        Second step, spin a graph amongst the buckets
        :return:
        '''
        buckets = defaultdict(set)

        # # Test data
        if self.test:
            line_iter = t_data

        # fetch data
        else:
            response = requests.get(self.uri)
            line_iter = response.iter_lines()
            next(line_iter)

        # parse words
        for line in line_iter:
            for word in line.split():
                word = word.decode("utf-8")
                self.all_words.add(word)

                for i in range(len(word)):
                    # create or get buckets of neighbors
                    bucket = word[:i] + '_' + word[i+1:]
                    buckets[bucket].add(word)

        print(f'found {len(self.all_words)} words')

        # second step
        for bucket in buckets:
            for word1 in buckets[bucket]:
                for word2 in buckets[bucket]:
                    if word1 != word2:
                        self.graph[word1].add(word2)
                        self.graph[word2].add(word1)
