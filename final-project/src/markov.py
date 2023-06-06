from collections import defaultdict
from nltk import ngrams
import random


class Markov:
    def __init__(self, midi_string, sequence_length):
        self.tokens = list(ngrams(midi_string.split(), sequence_length))
        self.d = defaultdict(list)

        for idx, i in enumerate(self.tokens[:-1]):
            self.d[i].append(self.tokens[idx + 1])

    def make_step(self, composition):
        choices = self.d.get(composition[-1], self.tokens)
        composition.append(random.choice(choices))

    def create_new_composition(self, output_length, last_token=None):
        composition = [last_token if last_token else random.choice(self.tokens)]

        while len(composition) < output_length:
            self.make_step(composition)

        return composition
