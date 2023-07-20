from gtts import gTTS
import PySimpleGUI as sg
import random
import pygame
from pygame import mixer, time
import os

layout = [
    [sg.Text("Thai Listening/Spelling Game")], 
    [sg.Text("This app will say 1 of the 500 most common Thai words and you must spell it down below!")],
    [sg.Text("", enable_events=True, key="-OUTPUT-")],
    [sg.Button('Listen Again', pad=(10, 10), key="-PLAY-"), sg.Text("Volume: "), sg.Slider(range=(0, 100), orientation='h', size=(20,8), enable_events=True, key="-VOLUME-", default_value=50)],
    [sg.Text("Type word here"), sg.Input(enable_events=True, key="-INPUT-")],
    [sg.Button("Submit", pad=(10,0), key="-SUBMIT-"), sg.Push(), sg.Button("Show Answer", pad=(10,0), key="-ANSWER-")] 
]
tool_window = sg.Window("Thai Practice", layout, finalize=True)

pygame.init()
mixer.init()

words_file = open("output.txt", mode='r', encoding="utf8")
word_list = words_file.readlines()


mytext = random.choice(word_list).strip()
lang = "th"
audio = gTTS(text=mytext, lang="th", slow=False)
audio.save("tts.mp3")
# os.system("start example.mp3")
mix_chan = mixer.Channel(0)

mix_chan.play(mixer.Sound("tts.mp3"))

while True:
    event, values = tool_window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "-PLAY-":
        mix_chan.play(mixer.Sound("tts.mp3"))
    if event == "-SUBMIT-":
        print(tool_window["-INPUT-"].get())
        print(mytext)
        if tool_window["-INPUT-"].get() == mytext:
            tool_window["-OUTPUT-"].update("Correct! The word was " + mytext)
        else:
            tool_window["-OUTPUT-"].update("That's not quite right")
    if event == "-ANSWER-":
        tool_window["-OUTPUT-"].update("The word was " + mytext)

tool_window.close()