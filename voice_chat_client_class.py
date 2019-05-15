#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:01:27 2019

@author: phoebeharmon
"""

import time
import socket
import select
import sys
import json
from chat_utils import *
import client_state_machine as csm

import threading

import speech_recognition as sr
from ibm_watson import SpeechToTextV1


class Client:
    def __init__(self, args):
        self.peer = ''
        self.console_input = []
        self.state = S_OFFLINE
        self.system_msg = ''
        self.local_msg = ''
        self.peer_msg = ''
        self.args = args

    def quit(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def get_name(self):
        return self.name

    def init_chat(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
        svr = SERVER if self.args.d == None else (self.args.d, CHAT_PORT)
        self.socket.connect(svr)
        self.sm = csm.ClientSM(self.socket)
        #reading_thread = threading.Thread(target=self.read_input) #???
        #trying for voice:
        reading_thread = threading.Thread(target=self.hear_input)

        reading_thread.daemon = True
        reading_thread.start()

    def shutdown_chat(self):
        return

    def send(self, msg):
        mysend(self.socket, msg)

    def recv(self):
        return myrecv(self.socket)

    def get_msgs(self):
        read, write, error = select.select([self.socket], [], [], 0)
        my_msg = ''
        peer_msg = []
        #peer_code = M_UNDEF    for json data, peer_code is redundant
        if len(self.console_input) > 0:
            my_msg = self.console_input.pop(0)
        if self.socket in read:
            peer_msg = self.recv()
        return my_msg, peer_msg

    def output(self):
        if len(self.system_msg) > 0:
            print(self.system_msg)
            self.system_msg = ''

    def login(self):
        my_msg, peer_msg = self.get_msgs()
        if len(my_msg) > 0:
            self.name = my_msg
            msg = json.dumps({"action":"login", "name":self.name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.state = S_LOGGEDIN
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(self.name)
                self.print_instructions()
                return (True)
            elif response["status"] == 'duplicate':
                self.system_msg += 'Duplicate username, try again'
                return False
        else:               # fix: dup is only one of the reasons
           return(False)


    def read_input(self):
        while True:
            text = sys.stdin.readline()[:-1] #stdin used for interactive input, it's a text file
            self.console_input.append(text) # no need for lock, append is thread safe
            #self.console_input is list of things the user types and enters'
    
    def hear_input(self):
        while True:
            text = self.voice_message()
            self.console_input.append(text)
    
    def voice_message(self):
        
        r = sr.Recognizer()

        #create instance of Microphone class
        mic = sr.Microphone()
        
# =============================================================================
#         #ibm
#         speech_to_text = SpeechToTextV1(iam_apikey = "", url = "")
#         with mic as source:
#             audio_file = r.adjust_for_ambient_noise(source)
#             audio_file = r.listen(source)
#             result = speech_to_text.recognize(audio = audio_file.get_wav_data(), content_type = 'audio/wav').get_result()
#             #response = json.dumps(result, indent=2)
#             message = result['results'][0]['alternatives'][0]['transcript']
# =============================================================================
        
        #google web api
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source) #records input until silence is detected
        
        #language option
        #if self.sm.language == 'english' else
        
        try:
            #language option
            if self.sm.language == "english":
                message = r.recognize_google(audio, language='en-us')
            elif self.sm.language == "chinese":
                message = r.recognize_google(audio, language='zh-cmn')
            
            #message = r.recognize_google(audio)
        except sr.RequestError:
            #API was unreachable or unresponsive
            message = "API unavailable"
        except sr.UnknownValueError:
            #speech was unintelligble
            message = ""
            
        return message
    

    def print_instructions(self):
        self.system_msg += menu

    def run_chat(self):
        self.init_chat()
        self.system_msg += 'Welcome to ICS chat\n'
        self.system_msg += 'Please enter your name: '
        self.output()
        while self.login() != True:
            self.output()
        self.system_msg += 'Welcome, ' + self.get_name() + '!'
        self.output()
        while self.sm.get_state() != S_OFFLINE:
            self.proc()
            self.output()
            time.sleep(CHAT_WAIT)
        self.quit()

#==============================================================================
# main processing loop
#==============================================================================
    def proc(self):
        my_msg, peer_msg = self.get_msgs()
        self.system_msg += self.sm.proc(my_msg, peer_msg)
