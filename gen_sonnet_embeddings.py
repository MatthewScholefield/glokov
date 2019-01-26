#!/usr/bin/env python3
from argparse import ArgumentParser
import re


def load_sonnets(filename):
    with open(filename) as f:
        passages = re.split(r'[IVCXL]+\n', f.read())
    return [
        [
            i.lower()
            for i in sum([re.findall(r'\w+', i) + [',']
                          for i in passage.split('\n') if i and not i.isspace()], [])
            if not re.search(r'^[IVCXL]+$', i)
        ]
        for passage in passages
        if passage and not passage.isspace()
    ]


def generate_embeddings(sonnets_filename, output_filename):
    from gensim.models import Word2Vec
    Word2Vec([
            ['^'] + words + ['$'] for words in load_sonnets(sonnets_filename)
        ], min_count=1).wv.save_word2vec_format(
        output_filename, binary=False
    )
    with open(output_filename) as f:
        lines = f.read().split('\n')
    with open(output_filename, 'w') as f:
        f.write('\n'.join(lines[1:]))


def main():
    parser = ArgumentParser()
    parser.add_argument('sonnets_file')
    parser.add_argument('output_embeddings_file')
    args = parser.parse_args()
    generate_embeddings(args.sonnets_file, args.output_embeddings_file)
    print('Wrote to {}!'.format(args.output_embeddings_file))


if __name__ == '__main__':
    main()
