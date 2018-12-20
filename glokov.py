#!/usr/bin/env python3
import random
import re
from argparse import ArgumentParser


def random_sample(options: dict) -> str:
    items = list(options.items())
    total = sum(i[1] for i in items)
    choice = random.random() * total
    chosen = 0
    while True:
        choice -= items[chosen][1]
        if choice <= 0:
            break
        chosen += 1
    return items[chosen][0]


def traverse_chain(chain, start_word=None, max_len=25):
    pos = ('.', start_word or '.')
    sentence = [start_word] * bool(start_word)
    while True:
        options = chain[pos]
        next_word = random_sample(options)
        sentence.append(next_word)
        if next_word == '.' or len(sentence) > max_len:
            return sentence
        pos = pos[1:] + (next_word,)


def create_chain(filename, lookback):
    with open(filename) as f:
        lines = sum([
            ['.'] * lookback + re.findall(r'\w+', i.lower()) + ['.']
            for i in f.read().split('\n')
        ], [])

    chain = {}
    for i in range(lookback, len(lines) - 1):
        word = lines[i]
        key = tuple(lines[i - lookback:i])
        entry = chain.setdefault(key, {})
        entry[word] = entry.get(word, 0) + 1
    del chain[('.',) * lookback]['.']
    return chain


def main():
    parser = ArgumentParser()
    parser.add_argument('input_file', help='Text file to read to generate similar sentences of')
    parser.add_argument('-n', '--num-sentences', type=int, default=3,
                        help='Number of sentences to generate')
    parser.add_argument('-f', '--first-word', help='First word of all sentences')
    args = parser.parse_args()

    chain = create_chain(args.input_file, 2)
    try:
        for i in range(args.num_sentences):
            print(' '.join(traverse_chain(chain, args.first_word)))
    except KeyError:
        print('The provided first word is not in the dataset:', args.first_word)


if __name__ == '__main__':
    main()
