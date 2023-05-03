from collections import defaultdict
from nltk import ngrams
import random


def markov(midi_string, sequence_length=6, output_length=250):
    d = defaultdict(list)
    tokens = list(ngrams(midi_string.split(), sequence_length))
    # store the map from a token to its following tokens
    for idx, i in enumerate(tokens[:-1]):
        d[i].append(tokens[idx + 1])
    # sample from the markov model
    l = [random.choice(tokens)]
    while len(l) < output_length:
        l.append(random.choice(d.get(l[-1], tokens)))
    # format the result into a string
    return ' '.join([' '.join(i) for i in l])
