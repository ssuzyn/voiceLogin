import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

def transform(filename, id, cnt):
    os.chdir("./static/uploads/" + id)
    print(os.getcwd())
    # print(os.listdir())
    # print(filename)
    pwd = cnt + '.png'
    signal, sr = librosa.load(filename)
    S_octave = librosa.feature.melspectrogram(signal, sr=sr, n_mels=128)
    librosa.display.specshow(librosa.power_to_db(S_octave, ref=np.max), sr=sr, y_axis='mel', x_axis='time')
    plt.ylim(0, 4000)
    plt.savefig(pwd)
    os.remove(filename)
    os.chdir("../../../") #원래 디렉토리 위치로 이동

def transformOne(filename, id):
    os.chdir("./static/login/" + id)
    print(os.getcwd())
    pwd = id + '.png'
    signal, sr = librosa.load(filename)
    S_octave = librosa.feature.melspectrogram(signal, sr=sr, n_mels=128)
    librosa.display.specshow(librosa.power_to_db(S_octave, ref=np.max), sr=sr, y_axis='mel', x_axis='time')
    plt.ylim(0, 4000)
    plt.savefig(pwd)
    os.remove(filename)
    os.chdir("../../../") #원래 디렉토리 위치로 이동

    return pwd