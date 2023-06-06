from music21.note import Note, Unpitched
from music21.midi.translate import streamToMidiFile
import music21
from fractions import Fraction
import io


def midi_to_string(midi_path):
    score = music21.converter.parse(midi_path)

    midi_string = ''
    last_offset = 0

    for note in score.flat.notes:
        if isinstance(note, Unpitched):
            continue

        delta_offset = note.offset - last_offset
        last_offset = note.offset
        if delta_offset:
            midi_string += 'p_{} '.format(delta_offset)

        duration = note.duration.components[0].type
        notes = [note] if isinstance(note, Note) else note.notes
        for n in notes:
            if isinstance(n, Unpitched):
                continue

            midi_string += 'n_{}_{} '.format(n.pitch.midi, duration)

    return midi_string


def composition_to_string(composition):
    midi_string = ' '.join(composition[0])
    for i in composition[1:]:
        midi_string += ' ' + i[-1]

    return midi_string


def string_to_midi(midi_string):
    stream = music21.stream.Stream()

    current_time = 1
    for token in midi_string.split():
        if token.startswith('n'):
            pitch, duration = token.lstrip('n_').split('_')
            note = Note(int(pitch))
            note.duration.type = duration
            stream.insert(current_time, note)

        elif token.startswith('p'):
            current_time += float(Fraction(token.lstrip('p_')))

    return streamToMidiFile(stream).writestr()


def create_byte_stream(midi_string):
    byte_stream = io.BytesIO()
    byte_stream.write(midi_string)
    byte_stream.seek(0)
    return byte_stream
