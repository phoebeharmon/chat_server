#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 14:44:26 2019

@author: phoebeharmon
"""

import speech_recognition as sr
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
import json
import threading

r = sr.Recognizer()

#create instance of Microphone class
mic = sr.Microphone()

#ibm
speech_to_text = SpeechToTextV1(iam_apikey = "", url = "")
with mic as source:
    audio_file = r.adjust_for_ambient_noise(source)
    audio_file = r.listen(source)
    result = speech_to_text.recognize(audio = audio_file.get_wav_data(), content_type = 'audio/wav', interim_results=True).get_result()
    #response = json.dumps(result, indent=2)
    print(result)
    message = result['results'][0]['alternatives'][0]['transcript']

print(message)