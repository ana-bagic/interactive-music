from music21.note import Note
import music21
from fractions import Fraction


def midi_to_string(midi_path):
    score = music21.converter.parse(midi_path)

    midi_string = ''
    last_offset = 0

    for note in score.flat.notes:
        delta_offset = note.offset - last_offset
        last_offset = note.offset
        if delta_offset:
            midi_string += 'p_{} '.format(delta_offset)

        duration = note.duration.components[0].type
        notes = [note] if isinstance(note, Note) else note.notes
        for n in notes:
            midi_string += 'n_{}_{} '.format(n.pitch.midi, duration)

    return midi_string


def string_to_midi(midi_string):
    stream = music21.stream.Stream()

    current_time = 1
    for token in midi_string.split():
        if token.startswith('n'):
            pitch, duration = token.lstrip('n_').split('_')
            note = music21.note.Note(int(pitch))
            note.duration.type = duration
            stream.insert(current_time, note)

        elif token.startswith('p'):
            current_time += float(Fraction(token.lstrip('p_')))

    return stream
