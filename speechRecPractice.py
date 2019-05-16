#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:29:10 2019

@author: phoebeharmon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:10:19 2019

@author: phoebeharmon
"""

import speech_recognition as sr
print(sr.__version__)

#Recognizer instance recongizes speech from an audio source
#create Recognizer instance
r = sr.Recognizer()

#7 methods to recognize speech from audio source
#only recognize_sphinx() works without internet connection
#default key provided for recognize_google() aka google web speech api
#r.recognize_google()

#AudioFile class initialized with path to an audio file
harvard = sr.AudioFile('harvard.wav')
with harvard as source: #context manager opens file, reads contents, stores data in AudioFile instance called source
    audio = r.record(source) #records data from file into AudioData instance
type(audio)

message = r.recognize_google(audio)
print(message)

#capture portion of speech in file
with harvard as source:
    audio1 = r.record(source, duration=4) #first 4 seconds of file
    audio2 = r.record(source, duration=4) #next 4 seconds of file
with harvard as source:
    audio3 = r.record(source, offset=4, duration=3) #records 3 seconds started at 4 seconds
message_4sec = r.recognize_google(audio)
print(message_4sec)

#deal with noise
with harvard as source:
    r.adjust_for_ambient_noise(source, duration=.5)
    audio = r.record(source)
    
print(r.recognize_google(audio, show_all = True)) #returns all possible transcripts