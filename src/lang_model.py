import pygame
from pygame import mixer

class Lang_Model():
    def __init__(self):
        pygame.init()
        mixer.init()
        self.lang_chan = mixer.Channel(0)

    def next_word():
        pass

    def get_word(self):     # word must be defined by child class
        return self.word
    
    def get_tran(self):     # tran (translation) must be defined by child class
        return self.tran
    
    def volume(self, num):
        self.lang_chan.set_volume(num/100)