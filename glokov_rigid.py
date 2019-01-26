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


def traverse_chain(chain, start_word=None, max_len=25, lookback=2):
    pos = ('.',) * (lookback - 1) + ((start_word or '^'),)
    sentence = [start_word] * bool(start_word)
    while True:
        options = chain[pos]
        next_word = random_sample(options)
        sentence.append(next_word)
        if next_word == '.' or len(sentence) > max_len:
            return sentence
        pos = pos[1:] + (next_word,)


def add_to_chain(chain, previous_words, next_word):
    key = tuple(previous_words)
    entry = chain.setdefault(key, {})
    entry[next_word] = entry.get(next_word, 0) + 1


def create_chain(filename, lookback):
    with open(filename) as f:
        lines = [
            i.lower()
            for i in f.read().split('\n')
            if not re.search(r'^[IVCXL]+$', i) and i
        ]

    line_words = [i for i in [re.findall(r'\w+', i) for i in lines] if i]

    chain = {}
    for i in range(1, len(lines)):
        if lines[i - 1][-1] == '.':
            add_to_chain(chain, ['.'] * (lookback - 1) + ['^'], line_words[i][0])

    lines = sum([
        ['.'] * lookback + words + ['.']
        for words in line_words if words
    ], [])

    for i in range(lookback, len(lines) - 1):
        add_to_chain(chain, lines[i - lookback:i], lines[i])
    del chain[('.',) * lookback]['.']
    return chain


def parse_latent_vector(line):
    word, *numbers = line.split()
    return word, list(map(float, numbers))


def load_embeddings(filename):
    with open(filename) as f:
        return dict(parse_latent_vector(line) for line in f)


def main():
    parser = ArgumentParser()
    parser.add_argument('input_file', help='Text file to read to generate similar sentences of')
    parser.add_argument('-n', '--num-sentences', type=int, default=3,
                        help='Number of sentences to generate')
    parser.add_argument('-f', '--first-word', help='First word of all sentences')
    parser.add_argument('-o', '--outline-file', help='Outline file with first words')
    args = parser.parse_args()

    chain = create_chain(args.input_file, 2)
    lines = []
    try:
        if args.outline_file:
            with open(args.outline_file) as f:
                first_words = [i.strip() for i in f.read().split('\n') if i.strip()]
            word_vars = {}
            for i, first_word in enumerate(first_words):
                if first_word.startswith('_'):
                    if first_word in word_vars:
                        first_words[i] = word_vars[first_word]
                    else:
                        first_words[i] = word_vars[first_word] = random_sample(chain[('.', '^')])
            for first_word in first_words:
                lines.append(' '.join(traverse_chain(chain, first_word.strip().lower())))
        else:
            for i in range(args.num_sentences):
                lines.append(' '.join(traverse_chain(chain, args.first_word.strip().lower())))
        lines = [i.replace(' .', ',').capitalize() for i in lines]
        lines[-1] = lines[-1].replace(',', '.')
        print('\n'.join(lines))
    except KeyError as e:
        print('The provided first word is not in the dataset:', e)


if __name__ == '__main__':
    main()
