import time
import PySimpleGUI as sg
from pygame import mixer
from src import Thai_Model

# Layout for title screen, currently only has play button
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

# Title screen main loop
while True:
    event, values = tool_window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        exit()
    if  event == "-START-":
        tool_window.close()
        break

# layout for the game window
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

lang = "th"     # When more languages are added, this will be set from the title screen and other models may be instantiated
if lang=="th":
    lang_model = Thai_Model()

effect_chan = mixer.Channel(1)  # Consider adding effect noises to Lang_Model

time.sleep(1)       # Wait a second before saying word so mixer finishes initializing
lang_model.play_sound()

while True:
    event, values = tool_window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "-PLAY-":
        lang_model.play_sound()
    
    # Check input
    if event == "-SUBMIT-" or event == "-ENTER-":
        # Correct case: Show word and meaning, say word again
        if tool_window["-INPUT-"].get() == lang_model.get_word():
            tool_window["-OUTPUT_MSG-"].update("Correct! The word was ")
            tool_window["-OUTPUT-"].update(lang_model.get_word())
            tool_window["-MEANING-"].update("Meaning: " + lang_model.get_tran())
            effect_chan.play(mixer.Sound("sounds/correct.mp3"))
        # Incorrect case: notify wrong, clear answer space, play dud sound
        else:
            tool_window["-OUTPUT_MSG-"].update("That's not quite right")
            tool_window["-OUTPUT-"].update("")
            effect_chan.play(mixer.Sound("sounds/dud.mp3"))

    # Show Answer and meaning
    if event == "-ANSWER-":
        tool_window["-OUTPUT_MSG-"].update("The word was ")
        tool_window["-OUTPUT-"].update(lang_model.get_word())
        tool_window["-MEANING-"].update("Meaning: " + lang_model.get_tran())

    # Update volume when volume slider is moved
    if event == "-VOLUME-":
        lang_model.volume(values["-VOLUME-"])
        effect_chan.set_volume(values["-VOLUME-"]/100)

    # New word: select new word from list, clear dynamic fields, say new word
    if event == "-NEW-":
        lang_model.next_word()
        tool_window["-OUTPUT_MSG-"].update("")
        tool_window["-OUTPUT-"].update("")
        tool_window["-INPUT-"].update("")
        tool_window["-MEANING-"].update("")
        lang_model.play_sound()

tool_window.close()