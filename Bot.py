#!/usr/bin/env python3
import requests
import time
import re
import json
import ApiKey
import os
from pydub import AudioSegment
LastUpdate = 0

APIAdd = f"https://api.telegram.org/bot{ApiKey.API}/"

def PostResponse(Chatid,Text,Markdown =False,Sender =""):
    if Markdown:
        Result = requests.get(f'{APIAdd}sendmessage?chat_id={Chatid}&parse_mode=MarkdownV2&text={Text}')
    else:
        print(f'{APIAdd}sendmessage?chat_id={Chatid}&text={Text}')
        Result = requests.get(f'{APIAdd}sendmessage?chat_id={Chatid}&text={Text}')
        print(Result)


def ParseMessage(message):
    Text = message["text"]
    Splits = re.split("\s",Text)
    if(Splits[1].lower() == "say"):
        Say(message)
    if(Splits[1].lower() == "check"):
        Check(message)
    if(Splits[1].lower() == "list"):
        ListSounds(message)

def Say(message):

    Text = message["text"]
    Splits = re.split("\s",Text)
    files = os.listdir("./Sounds")
    if(len(Splits)<= 2):
        return
    combined = AudioSegment.from_file(f'./Sounds/_period.wav',format="wav")
    Textcmb = ""
    for i in range(2,len(Splits)):
        if(f'{Splits[i].lower()}.wav' in files):
            sound = AudioSegment.from_file(f'./Sounds/{Splits[i].lower()}.wav',format="wav")
            combined = combined + sound
            Textcmb = f'{Textcmb} {Splits[i].lower()}'
        else:
            sound = AudioSegment.from_file(f'./Sounds/error.wav',format="wav")
            combined = combined + sound
            Textcmb = f'{Textcmb} ERROR'
    combined.export("./tmp/tmp.mp3",format="mp3")
    url = f'{APIAdd}sendDocument?chat_id={message["chat"]["id"]}'
    payload={}
    files=[
        ('document',(f'{Textcmb}.mp3',open(f'./tmp/tmp.mp3','rb'),'audio/mp3'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)


def Check(message):
    Text = message["text"]
    Splits = re.split("\s",Text)
    if(len(Splits)>2):
        files = os.listdir("./Sounds")
        has=any(file in f'{Splits[2].lower()}.wav' for file in files)
        PostResponse(Update["message"]["chat"]["id"],has)

def ListSounds(message):
    files = os.listdir("./Sounds")
    List = "all Sound Files:\n"
    count = 0
    files.sort();

    Splits = re.split("\s",Text)
    if(len(Splits) == 3 and len(Splits[2]) == 1):
        files = [file for file in files if file[0].lower() == Splits[2].lower()]
    for f in files:
           count=count+1
           List=f'{List} · {f[:-4]}'
           if(count>100):
               PostResponse(Update["message"]["chat"]["id"],List)
               List = ""
               count = 0
    PostResponse(Update["message"]["chat"]["id"],List)

while True:

    Result = requests.get(f'{APIAdd}getUpdates?offset={LastUpdate}')
    Updates = Result.json()
    for Update in Updates["result"]:
        LastUpdate = Update["update_id"]+1
        if "message" in Update:
            if "text" in Update["message"]:
                Text = Update["message"]["text"]
                if bool(re.search("^/voxbot ",Text.lower())):
                    ParseMessage(Update["message"])


    time.sleep(.1000)
