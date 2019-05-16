#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:37:27 2019

@author: phoebeharmon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:41:00 2019
@author: phoebeharmon
"""

import speech_recognition as sr
r = sr.Recognizer()

#create instance of Microphone class
mic = sr.Microphone()

#if your system does not have default microphone:
#print(sr.Microphone.list_microphone_names())
#mic = sr.Microphone(device_index=3) #uses microphone with index 3 on list of microphones

with mic as source:
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source) #records input until silence is detected

try:
    message = r.recognize_google(audio, language='zh-cmn')
except sr.RequestError:
    #API was unreachable or unresponsive
    message = "API unavailable"
except sr.UnknownValueError:
    #speech was unintelligble
    message = "Unable to recognize speech"
print(message)