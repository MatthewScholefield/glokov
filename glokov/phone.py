# -*- coding: UTF-8 -*-
import json
import requests
from lazy import lazy
from os.path import join, isfile
from tempfile import gettempdir


class Phonemes:
    cmubet_to_ipa = {
        'AA': 'ɑ', 'AE': 'æ', 'AH': 'ʌ', 'AO': 'ɔ', 'AW': 'ɑʊ', 'AY': 'ɑɪ', 'B': 'b', 'CH': 'ʧ',
        'D': 'd', 'DH': 'ð', 'EH': 'ɛ', 'ER': 'ɜɹ', 'EY': 'eɪ', 'F': 'f', 'G': 'ɡ', 'HH': 'h',
        'IH': 'i', 'IY': 'ɪː', 'JH': 'ʤ', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'NG': 'ŋ',
        'OW': 'oʊ', 'OY': 'ɔɪ', 'P': 'p', 'R': 'ɹ', 'S': 's', 'SH': 'ʃ', 'SIL': '.', 'T': 't',
        'TH': 'θ', 'UH': 'ʊ', 'UW': 'u', 'V': 'v', 'W': 'w', 'Y': 'j', 'Z': 'z', 'ZH': 'ʒ'
    }

    def __init__(self, filename=None, url=None):
        self.filename = filename or join(gettempdir(), 'cmudict.json')
        self.url = url or 'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b'

    def get_stresses(self, word):
        return [i for i in self.get_all_stresses(word) if i is not None]

    def get_all_stresses(self, word):
        return [int(w[-1]) if w[-1].isdigit() else None for w in self.get_raw_phones(word)]

    def get_raw_phones(self, word):
        phones_str = self.words.get(word.upper())
        return phones_str.split(' ') if phones_str else []

    def get_phones(self, word):
        return [i[:-1] if i[-1].isdigit() else i for i in self.get_raw_phones(word)]

    def get_ipa(self, word):
        return ''.join(self.cmubet_to_ipa[phone] for phone in self.get_phones(word))

    @lazy
    def rhyme_suffixes(self):
        return {word: self._calc_rhyme_suffix(word) for word in self.words}

    @lazy
    def words(self):
        if not isfile(self.filename):
            with open(self.filename, 'w') as f:
                json.dump(self._download(), f)
        with open(self.filename) as f:
            return json.load(f)

    def get_rhymes(self, word):
        word_suffix = self.rhyme_suffixes[word.upper()]
        return [
            i
            for i, i_suffix in self.rhyme_suffixes.items()
            if i_suffix == word_suffix and i != word.upper()
        ]

    def _calc_rhyme_suffix(self, word):
        phones = []
        for phone, stress in zip(self.get_phones(word), self.get_all_stresses(word)):
            if stress and stress > 0:
                phones = []
            phones.append((phone, stress))
        return phones

    def _download(self):
        file_data = requests.get(self.url).text
        data = [i for i in file_data.split('\n') if not i.startswith(';;;')]
        return {line.split()[0]: ' '.join(line.split()[1:]) for line in data if
                len(line.split()) > 1}
