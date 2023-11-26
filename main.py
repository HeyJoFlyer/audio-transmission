import time
import wave
import numpy as np
import os
import os.path
import sys
import bitarray


volume = 0.5
samples_per_second = 2000
channels = 1
ontime = 0.2
frequency_1 = 440
offtime = 0.1
frequency_0 = 690

def do(input : str):
    bits = bitarray.bitarray()
    bits.frombytes(input.encode('utf-8'))
    total_len = len(bits) * ontime + ((len(bits) - 1) * offtime)
    total_samples = total_len * samples_per_second
    t = np.linspace(0, ontime, int(samples_per_second * ontime))
    t_off = np.linspace(0, 0, int(samples_per_second * offtime))
    raw_audio_1 = 0.5 * np.sin(2 * np.pi * frequency_1 * t)
    raw_audio_0 = 0.5 * np.sin(2 * np.pi * frequency_0 * t)
    list_audio = []
    raw_audio = np.empty(shape=(1, 1))
    for bit in bits:
        if bit == 0:
            list_audio.append(raw_audio_1)
            list_audio.append(t_off)
        elif bit == 1:
            list_audio.append(raw_audio_0)
            list_audio.append(t_off)
        else:
            print("Well it looks like that wasnt'actually binary")
    total_array = np.concatenate(list_audio)
    write_file(total_array)
def write_file(raw_audio):
    folder = os.path.dirname(sys.argv[0])
    audiofile = os.path.join(folder, "bdt.wav")
    audio = (raw_audio * (2 ** 15 - 1)).astype("<h")
    #print(audio)
    with wave.open(audiofile, "w") as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(samples_per_second)
        file.writeframes(audio.tobytes())

do("hello world")

