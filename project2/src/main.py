import random

from midiStringConverter import string_to_midi, midi_to_string
from markov import Markov

midi_files = ['time', 'kiss-the-rain', 'river-flows-in-you', 'pirate']
sequence_length = 3
output_length = 3000
change_rate = 0.01

midi_strings = [midi_to_string('base-midi/' + midi + '.mid') for midi in midi_files]

markovs = [Markov(midi, sequence_length) for midi in midi_strings]
composition = []
current_markov = random.choice(markovs)
current_markov.start_composition(composition)

while len(composition) < output_length:
    if random.uniform(0, 1) <= change_rate:
        current_markov = random.choice(markovs)
    current_markov.make_step(composition)

final_string = ' '.join(composition[0])
for i in composition[1:]:
    final_string += ' ' + i[-1]
generated_midi = string_to_midi(final_string)
generated_midi.write('midi', 'generated-midi/generated.mid')
