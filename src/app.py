# bibliotecas para interface front e backend
from __future__ import unicode_literals
from distutils.log import debug
from tempfile import SpooledTemporaryFile
import eel
import os

# bibliotecas para análise facial
from deepface import DeepFace
from time import sleep, perf_counter
import pandas as pd
import cv2

# biblioteca para acessar explorador de arquivo
import subprocess

# bibliotecas para gráficos
import collections

# definição do caminho frontend
eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')
path = f'{os.path.dirname(os.path.realpath(__file__))}\Results'


class FaceAnalyzer():
    def __init__(self, capture):
        self.capture = capture
        if not self.capture.isOpened():
            raise IOError("Não foi possível acessar webcam")
        else:
            self.start = perf_counter()
            self.current_reaction = 'neutral'
            self.new_reaction = 'neutral'
            self.face_found = False
            self.reactions = [(self.current_reaction, 0)]
            self.reactions_step = []
            self.sorted_frequency_list = []
            self.faceCascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_reaction(self):
        '''Verifica video da webcam buscando por expressões faciais'''

        try:
            success, self.frame = self.capture.read()
            predictions = DeepFace.analyze(self.frame, actions=['emotion'])
            self.new_reaction = predictions["dominant_emotion"]
            print(self.new_reaction)
            self.face_found = True
        except:
            print("Face not detected...")
            self.face_found = False

    def show_faces(self):
        '''Exibe faces detectadas na webcam com suas expressões'''

        if self.face_found == True:
            faces = self.faceCascade.detectMultiScale(self.frame, 1.1, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(self.frame, self.new_reaction, (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)
            cv2.startWindowThread()
            cv2.imshow('FaceAnalyzer', self.frame)
            cv2.waitKey(1)

    def check_reaction(self):
        '''Verifica se há nova reação e adiciona à lista de reações'''

        if self.new_reaction != self.current_reaction:
            self.current_reaction = self.new_reaction
            running_time = perf_counter() - self.start
            self.reactions.append((self.new_reaction, running_time))

    def check_stop(self, debug_mode):
        '''Verifica se usuário deseja parar e salva reações no arquivo'''

        if debug_mode == True:
            exitApp = eel.checkDebugButton()()
        else:
            exitApp = eel.checkRunButton()()
        if exitApp:
            running_time = perf_counter() - self.start
            self.reactions.append((self.current_reaction, running_time))
            self.create_step_reactions_list()
            self.create_frequency_list()
            print(f'\n{self.reactions = }')
            print(f'\n{self.reactions_step = }')
            print(f'\n{self.sorted_frequency_list = }')
            results = pd.DataFrame(self.reactions)
            results.to_excel(f"{path}/Results.xlsx", sheet_name='Expressões detectadas')
            return True

    def create_step_reactions_list(self):
        '''Cria lista com reações por segundo'''

        current_reaction = 'neutral'
        step = 0
        for reaction in self.reactions:
            while step < reaction[1]:
                self.reactions_step.append((current_reaction, step))
                step += 1
            current_reaction = reaction[0]
        self.reactions_step.append((reaction[0], step))

    def create_frequency_list(self):
        '''Cria lista com frequência de reações'''

        reactions_list = [reaction[0] for reaction in self.reactions_step]
        frequency_list = list(collections.Counter(reactions_list).items())
        self.sorted_frequency_list = sorted(frequency_list, key=lambda x: (-x[1], x[0]))


def start(debug_mode):
    '''Inicia modo debug'''

    capture = cv2.VideoCapture(0)
    fa = FaceAnalyzer(capture)
    while True:
        fa.detect_reaction()
        if debug_mode == True:
            fa.show_faces()
        fa.check_reaction()
        stop_running = fa.check_stop(debug_mode)
        if stop_running == True:
            break
        sleep(1)
    capture.release()
    cv2.destroyAllWindows()


@eel.expose
def run():
    start(debug_mode=False)


@eel.expose
def debug():
    start(debug_mode=True)


@eel.expose
def open_results():
    '''Abre pasta contendo arquivo de resultados'''

    subprocess.Popen(f'explorer "{path}"')


eel.start('index.html', size=(620, 235))
