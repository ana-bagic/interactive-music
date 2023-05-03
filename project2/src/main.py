from midiStringConverter import string_to_midi, midi_to_string
from toMarkov import markov

midi_file = 'yiruma'
sequence_length = 6
output_length = 1000

midi_string = midi_to_string('base-midi/' + midi_file + '.mid')
generated_midi = string_to_midi(markov(midi_string, sequence_length, output_length))
generated_midi.write('midi', 'generated-midi/' + midi_file + '.mid')
