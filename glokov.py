#!/usr/bin/env python3
from numpy import random

from argparse import ArgumentParser
from typing import List

from clustering import cluster_points
from gen_sonnet_embeddings import load_sonnets
from glokov_rigid import add_to_chain, random_sample
import numpy as np


def parse_embedding(line):
    word, *numbers = line.split()
    return word, np.array(list(map(float, numbers)))


def load_embeddings(filename):
    with open(filename) as f:
        return dict(parse_embedding(line) for line in f)


class CentroidChainPool:
    def __init__(self, embeddings: dict, num_clusters: int, sentences: list):
        self.embeddings = embeddings
        embedding_items = list(embeddings.items())
        kmeans = cluster_points([v for k, v in embedding_items], num_clusters)
        self.clusters = kmeans.cluster_centers_
        print(kmeans.labels_)
        self.word_to_cluster = {
            word: cluster_id for (word, _), cluster_id in zip(embedding_items, kmeans.labels_)
        }
        self.cluster_to_words = {}
        for word, cluster_id in self.word_to_cluster.items():
            self.cluster_to_words.setdefault(cluster_id, set()).add(word)
        self.chains = {}
        for sentence in ['^'] + sentences + ['$']:
            for i in range(1, len(sentence)):
                prev_indices = [self.word_to_cluster[j] for j in sentence[i - 1:i]]
                add_to_chain(self.chains, prev_indices, self.word_to_cluster[sentence[i]])

    def get_residual_embeddings(self) -> dict:
        return {
            word: point - self.clusters[self.word_to_cluster[word]]
            for word, point in self.embeddings.items()
        }


class Glokov:
    def __init__(self):
        self.embeddings = {}
        self.pools = []  # type: List[CentroidChainPool]

    def generate(self, input_file, embeddings_file, num_levels=1, num_clusters=50):
        self.embeddings = embeddings = load_embeddings(embeddings_file)
        sentences = load_sonnets(input_file)
        self.pools = []
        for level in range(num_levels):
            chain_pool = CentroidChainPool(embeddings, num_clusters, sentences)
            self.pools.append(chain_pool)
            embeddings = chain_pool.get_residual_embeddings()

    def create_sentence(self, start_word='^', stop_word='$') -> list:
        prev_word = start_word
        origin_pos = np.zeros(next(iter(self.embeddings.values())).shape)
        sentence = []

        if start_word != '^':
            sentence.append(start_word)

        while True:
            word_pos = origin_pos
            possible_words = set(self.embeddings)

            for pool in self.pools:
                cluster_id = pool.word_to_cluster[prev_word]
                options = pool.chains[(cluster_id,)]
                next_cluster = random_sample(options)
                word_pos += pool.clusters[next_cluster]

                possible_words &= pool.cluster_to_words[next_cluster]
                # words_left = possible_words & pool.cluster_to_words[next_cluster]
                # if words_left:
                #     possible_words = words_left
                # print(words_left)

            print(possible_words)
            # next_word = random.choice(list(possible_words))
            words = list(self.embeddings)
            next_word = random_sample({
                word: 1 / np.sum(np.square(self.embeddings[word] -word_pos))
                for word in words
            })
            if next_word == stop_word or len(sentence) > 25:
                return sentence
            sentence.append(next_word)
            prev_word = next_word


def main():
    parser = ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('embeddings_file')
    args = parser.parse_args()
    glokov = Glokov()
    glokov.generate(args.input_file, args.embeddings_file)
    print(' '.join(glokov.create_sentence()))


if __name__ == '__main__':
    main()
