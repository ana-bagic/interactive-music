import random

from midiStringConverter import string_to_midi, midi_to_string
from markov import Markov

midi_file1 = 'river-flows-in-you'
midi_file2 = 'kiss-the-rain'
sequence_length = 6
output_length = 900
change_rate = 0.1

midi_string1 = midi_to_string('base-midi/' + midi_file1 + '.mid')
midi_string2 = midi_to_string('base-midi/' + midi_file2 + '.mid')

markovs = [Markov(midi_string1, sequence_length), Markov(midi_string2, sequence_length)]
composition = []
current_markov = random.choice(markovs)
current_markov.start_composition(composition)

while len(composition) < output_length:
    if random.uniform(0, 1) <= change_rate:
        current_markov = random.choice(markovs)
    current_markov.make_step(composition)

final_string = ' '.join([' '.join(i) for i in composition])
generated_midi = string_to_midi(final_string)
generated_midi.write('midi', 'generated-midi/generated.mid')
