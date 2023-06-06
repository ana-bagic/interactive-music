import random

from util import midi_to_string, composition_to_string, string_to_midi, create_byte_stream
from markov import Markov
import pygame
from fer import FER
import cv2

# emotion detection
video = cv2.VideoCapture(0)
emotion_detector = FER(mtcnn=True)

# music player
MUSIC_END = pygame.USEREVENT + 1
pygame.init()
pygame.mixer.init(44100, -16, 2, 1024)
pygame.mixer.music.set_endevent(MUSIC_END)

# markov chains
files = {'happy': ['river-flows-in-you', 'clocks', 'dancing-queen'],
         'sad': ['kiss-the-rain', 'gymnopedie'],
         'angry': ['pirate', 'gladiator', 'in-the-end'],
         'neutral': ['time', 'mid6']}
token_length = 3
output_length = 500

happy_strings = [midi_to_string('midi/' + midi_file + '.mid') for midi_file in files.get('happy')]
sad_strings = [midi_to_string('midi/' + midi_file + '.mid') for midi_file in files.get('sad')]
angry_strings = [midi_to_string('midi/' + midi_file + '.mid') for midi_file in files.get('angry')]
neutral_strings = [midi_to_string('midi/' + midi_file + '.mid') for midi_file in files.get('neutral')]
markovs = {'happy': [Markov(midi_string, token_length) for midi_string in happy_strings],
           'sad': [Markov(midi_string, token_length) for midi_string in sad_strings],
           'angry': [Markov(midi_string, token_length) for midi_string in angry_strings],
           'neutral': [Markov(midi_string, token_length) for midi_string in neutral_strings]}
markov = random.choice(markovs.get('happy'))


def generate_new_midi(last_token=None):
    composition = markov.create_new_composition(output_length, last_token)
    final_string = composition_to_string(composition)
    generated_midi = string_to_midi(final_string)
    return create_byte_stream(generated_midi), composition[-1]


def reset_play():
    stream1, token = generate_new_midi()
    stream2, token = generate_new_midi(token)
    pygame.mixer.music.load(stream1)
    pygame.mixer.music.queue(stream2)
    pygame.mixer.music.play()
    return token


# emotions change
prev_emotion = ''
current_emotion = ''
CHANGE_ERROR = 4
counter = 0

prev_token = reset_play()
while True:
    success, img = video.read()

    analysis = emotion_detector.top_emotion(img)[0]
    if analysis in markovs.keys():
        if analysis != current_emotion:
            counter = 0
            current_emotion = analysis
        elif counter < CHANGE_ERROR:
            counter += 1
            if counter == CHANGE_ERROR and current_emotion != prev_emotion:
                prev_emotion = current_emotion
                print('change to', prev_emotion)

                markov = random.choice(markovs.get(prev_emotion))
                prev_token = reset_play()

    for event in pygame.event.get():
        if event.type == MUSIC_END:
            stream, prev_token = generate_new_midi(prev_token)
            pygame.mixer.music.queue(stream)

    cv2.imshow("webcam", img)
    cv2.waitKey(1)
