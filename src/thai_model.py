import random
import sys
from gtts import gTTS
from pygame import mixer, time

sys.path.append('../wordlists')
sys.path.append('../sounds')

from .lang_model import Lang_Model

class Thai_Model(Lang_Model):
    def __init__(self):
        super().__init__()
        self.word_meaning_pairs=self.intake_words()
        self.next_word()

    def next_word(self):
        word_pair = random.choice(self.word_meaning_pairs)
        self.word = word_pair[0]
        self.tran = word_pair[1]
        audio = gTTS(text=word_pair[0], lang='th', slow=False)
        audio.save("sounds/th_tts.mp3")
        

    def play_sound(self):
        self.lang_chan.play(mixer.Sound("sounds/th_tts.mp3"))
    
    def intake_words(self):
        words_file = open("wordlists/thai_words.txt", mode='r', encoding="utf8")
        word_list = words_file.readlines()
        word_meaning_pairs = []
        for line in word_list:
            pair = line.split()
            word_meaning_pairs.append([pair[0], pair[1]])
        return word_meaning_pairs