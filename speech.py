import pyglet
from gtts import gTTS
import os
import time


# this is google text to speech api provided bt gtts and then this speech is play in the
# form of .mp3 file by pyglet framework

def ttspeech(text, lang) :

    file = gTTS(text=text, lang=lang,slow=False)

    filename = 'F:/voice assistant/temp.mp3'
    file.save(filename)

    music = pyglet.media.load(filename, streaming = False)
    music.play()

    time.sleep(music.duration)
    os.remove(filename)








