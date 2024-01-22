import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import os
import gc
from time import*

from plyer import notification

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))
    
def form(a):
    kush=["{", "\n", '  "partial" : "', '"', "}"]
    for i in kush:
        a=a.replace(i, "")
    return(a)

def node(text):
     notification.notify(
        title="абоба",
        message=text,
        app_name="YourAppName",
        app_icon=None,
        timeout=10
     )

def vois():
    devices = sd.query_devices()
    default_input_device = devices[0]["name"]
    samplerate = devices[0]["default_samplerate"]
    path=["vosk-model-en-us-daanzu-20200905-lgraph", "data/data/vosk-model-en-us-daanzu-20200905-lgraph"]
    for i in range(ord('A'), ord('Z') + 1):
        i=chr(i)
        if os.path.exists(f"{i}:\\{path[0]}"):
             model = Model(f"{i}:/{path[0]}")
             break
    else:
        if os.path.exists(path[1]):
            model = Model(path[1])
        else: model = Model("/storage/emulated/0/vosk-model-en-us-daanzu-20200905-lgraph")

    with sd.InputStream(device=default_input_device, samplerate=samplerate, blocksize=8000,
                    dtype='int16', channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            q.queue.clear()
            if rec.AcceptWaveform(data):
                gc.collect()
                rec.Reset()
            else:
                if form(rec.PartialResult())!="":
                    node(form(rec.PartialResult()))
                       
vois()
