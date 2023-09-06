import PySimpleGUI as sg
import cv2
from pytesseract import image_to_string
from googlesearch import search
import requests
import pandas as pd
from bs4 import *
import time
import pyttsx3
import speech_recognition as sr

def reno():
    """
    The function `reno()` uses the SpeechRecognition library in Python to listen for audio input from
    the user, convert it to text using Google's speech recognition API, and return the recognized text.
    :return: The function `reno()` returns the text that is recognized from the user's audio input,
    converted to lowercase.
    """
    try:
        while True:
            sample_rate = 48000
            chunk_size = 2048
            r = sr.Recognizer()
            mic_list = sr.Microphone.list_microphone_names()

            with sr.Microphone( sample_rate=sample_rate,
                               chunk_size=chunk_size) as source:
                # wait for a second to let the recognizer adjust the
                # energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source)
                print("Say Something")
                # listens for the user's input
                audio = r.listen(source)

                try:
                    text = r.recognize_google(audio)
                    return text.lower()

                except sr.UnknownValueError:
                    speech("Sorry,could not understand audio")

    except:
        speech("check your network connection")

def speech(text):
    """
    The `speech` function uses the pyttsx3 library to convert text into speech using the default voice.
    
    :param text: The `text` parameter is the text that you want the speech engine to speak out loud
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def heart(text):
    links=[]
    k=[]
    detail = " "
    df = pd.read_csv(r"E:\jupyterfiles\jupyter\jupyter\druglist.csv")
    search_word = text + "1mg"

   # The code block you provided is performing the following tasks:
    try:
      for j in search(search_word, num_results=1):
        links.append(j)
        time.sleep(1)
        req = requests.get(links[0])
    except:
        matching_rows = df[df["drug"].str.contains(search_word)]
        for j in search(matching_rows.iloc[0], num_results=1):
            links.append(j)
            time.sleep(1)
            req = requests.get(links[0])


    soup=BeautifulSoup(req.content,"html.parser")
    a=soup.get_text().lower()
    s=0
    name=["used in","benefits","uses of ","common side effects of","Uses and benefits","is used for"]
    for l in name:
        if(a.find(l)):
            s=a.find(l)
            x = a.find("moreread")
            m=soup.get_text()[s:x].strip("\n")
            x=m.find("1mg")
            n=soup.get_text()[s:x].strip("\n")
            o=n.find("₹")
            k.append(soup.get_text()[s:o].strip("\n"))
        else:
            k.append(soup.get_text()[s:].strip("\n"))
    for e in k:
        detail += e
    return detail


def lens():
    """
    The function `lens()` captures video from the webcam, resizes the frames, converts them to text
    using OCR, and returns the result to the `heart()` function.
    :return: the result of the `heart(a)` function call.
    """
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        frame = cv2.resize(frame, (1366, 768))
        a = image_to_string(frame)
        if a != None and a != " ":
            return heart(a)




sg.theme("Light Blue 2")

font = ("Times of Roman", 19)
layout = [
        [sg.Text('                   MEDICINE DESCRIBER', size=(80, 3), key='-bold-', font=("Merriweather",30))],
        #[sg.Image('wa.GIF', size=(800, 400),pad=(200,0))],
        [sg.Text('MEDICINE NAME', size=(15,1),pad=(5,0),font=font), sg.InputText(font=font)],
        [sg.Button('Search', pad=(100, 10), size=(8, 2), font=font),sg.Button('lens', pad=(50, 10), size=(8, 2), font=font),sg.Button('Read', pad=(50, 10), size=(8, 2), font=font)],
        #[sg.Button('lens',size=(8,2),font=font,pad=(150,45))]
        [sg.Multiline(size=(500, 10), font=('Tahoma', 13),  autoscroll=True,key="-OUTPUT-", disabled=True),sg.VerticalSeparator(pad=None) ],
        [sg.Button('Exit', size=(15, 1), pad=(5, 0), font=font),sg.Button('Voice', size=(15, 1), pad=(5, 0), font=font)]
]

window = sg.Window(" ", layout,size=(895, 640))


while True:  # Event Loop
    event, values = window.read()
    try:
        text=values[0]
        if event == "lens":
            try:
                window["-OUTPUT-"].update(lens())
            except:
                None

        elif event == "Search":
            window["-OUTPUT-"].update(heart(text))

        elif event == "Read":
            if text!=None:
                speech(heart(text))

        elif event == "Voice":
            try:
                window["-OUTPUT-"].update(heart(reno()))
            except:
                pass

    except:
        None

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()