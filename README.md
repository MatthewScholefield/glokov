# Glokov

Glokov uses simple markov chains to do sentence generation. You provide an example dataset and it
 reads it, generating example sentences based around the provided text.
 
## Usage
 
```bash
$ python3 glokov.py --help
usage: glokov.py [-h] [-n NUM_SENTENCES] [-f FIRST_WORD] input_file

positional arguments:
  input_file            Text file to read to generate similar sentences of

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_SENTENCES, --num-sentences NUM_SENTENCES
                        Number of sentences to generate
  -f FIRST_WORD, --first-word FIRST_WORD
                        First word of all sentences
 ```
 
 Example:
```bash
$ python3 glokov.py data/shakespeare.txt -n 3 -f the
the eyes fore duteous now converted are .
the uncertain sickly appetite to please him thou art blam d if thou wouldst convert .
the expense of many lives upon his gains .
```
