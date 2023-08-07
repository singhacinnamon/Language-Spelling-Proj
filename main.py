from gtts import gTTS
import PySimpleGUI as sg
import random
import pygame
from pygame import mixer, time
import os

from src import Lang_Model, Thai_Model

title_layout = [
    [sg.Push(), sg.Text("Thai Listening/Spelling Game", font=("arial_black", 35)), sg.Push()], 

    [sg.Push(), sg.Text("This app will say 1 of the 500 most common Thai words and you must spell it down below!\nIf you are stuck, you may show the answer and/or skip to the next word", justification="center"), sg.Push()],

    [sg.Text("")],
    [sg.Text("")],
    [sg.Text("")],
    [sg.Text("")],

    [sg.Push(), sg.Text("Good luck and have fun!", font=(30), justification="center"), sg.Push()],

    [sg.Push(), sg.Button("Play", key="-START-", size=(10, 2), font=(20)), sg.Push()]
]

tool_window = sg.Window("Language Practice", title_layout, finalize=True, size=(700, 400))

while True:
    event, values = tool_window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        exit()
    if  event == "-START-":
        tool_window.close()
        break

layout = [
    [sg.Push(), 
     sg.Text("Listen, Spell!", font=("arial_black", 30)), 
     sg.Push()],

    [sg.Push(),
     sg.Text("", enable_events=True, key="-OUTPUT_MSG-", font=(25)),
     sg.Push()],

    [sg.Push(), 
     sg.Text("", enable_events=True, key="-OUTPUT-", text_color=("lime"), font=("unesco", 60)),
     sg.Push()],

     [sg.Push(),
      sg.Text("", key="-MEANING-"), 
      sg.Push()],

    [sg.Push(), 
     sg.Button('Listen Again', pad=(10, 10), key="-PLAY-"), sg.Text("Volume: "), 
     sg.Slider(range=(0, 100), orientation='h', size=(20,8), enable_events=True, key="-VOLUME-", default_value=50), 
     sg.Push()],

    [sg.Push(), 
     sg.Input(key="-INPUT-", size=(50,5), justification="center", font=30), 
     sg.Push()],

    [sg.Push(), 
     sg.Button("Submit", pad=(10,0), key="-SUBMIT-", size=(12,2), button_color="green", ), 
     sg.Button("Show Answer", pad=(10,0), key="-ANSWER-", button_color="#e41429", size=(12,2)), 
     sg.Button("Next Word", pad=(10,0), key="-NEW-", size=(12,2)),
     sg.Push()] 
]


tool_window = sg.Window("Thai Practice", layout, finalize=True, size=(700, 400))
tool_window["-INPUT-"].bind("<Return>", "-ENTER-")

lang = "th"
if lang=="th":
    lang_model = Thai_Model()

effect_chan = mixer.Channel(1)

lang_model.play_sound()

while True:
    event, values = tool_window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "-PLAY-":
        lang_model.play_sound()
    
    if event == "-SUBMIT-" or event == "-ENTER-":
        print(tool_window["-INPUT-"].get())
        print(lang_model.get_word())
        if tool_window["-INPUT-"].get() == lang_model.get_word():
            tool_window["-OUTPUT_MSG-"].update("Correct! The word was ")
            tool_window["-OUTPUT-"].update(lang_model.get_word())
            tool_window["-MEANING-"].update("Meaning: " + lang_model.get_tran())
            effect_chan.play(mixer.Sound("sounds/correct.mp3"))
        else:
            tool_window["-OUTPUT_MSG-"].update("That's not quite right")
            tool_window["-OUTPUT-"].update("")
            effect_chan.play(mixer.Sound("sounds/dud.mp3"))

    if event == "-ANSWER-":
        tool_window["-OUTPUT_MSG-"].update("The word was ")
        tool_window["-OUTPUT-"].update(lang_model.get_word())
        tool_window["-MEANING-"].update("Meaning: " + lang_model.get_tran())

    if event == "-INPUT-" and tool_window["-INPUT-"].get() == "Type word here":
        tool_window["-INPUT-"].update("")

    if event == "-VOLUME-":
        lang_model.volume(values["-VOLUME-"])
        effect_chan.set_volume(values["-VOLUME-"]/100)

    if event == "-NEW-":
        lang_model.next_word()
        tool_window["-OUTPUT_MSG-"].update("")
        tool_window["-OUTPUT-"].update("")
        tool_window["-INPUT-"].update("")
        tool_window["-MEANING-"].update("")
        lang_model.play_sound()

tool_window.close()