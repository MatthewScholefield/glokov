import requests


def download_phonemes() -> dict:
    file_data = requests.get(
        'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b').text
    data = [i for i in file_data.split('\n') if not i.startswith(';;;')]
    return {line.split()[0]: ' '.join(line.split()[1:]) for line in data if len(line.split()) > 1}

