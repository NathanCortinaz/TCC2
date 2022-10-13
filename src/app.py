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

# definição do caminho frontend
eel.init(f'{os.path.dirname(os.path.realpath(__file__))}/web')
path = f'{os.path.dirname(os.path.realpath(__file__))}\Results'


class FaceAnalyzer():
    def __init__(self, capture, exit_character='q'):
        self.capture = capture
        if not self.capture.isOpened():
            raise IOError("Não foi possível acessar webcam")
        else:
            self.start = perf_counter()
            self.current_reaction = 'neutral'
            self.new_reaction = 'neutral'
            self.face_found = False
            self.reactions = [(self.current_reaction, 0)]
            self.faceCascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.exit_character = exit_character

    def detect_reaction(self):
        '''Check webcam video looking for face expressions'''
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
        '''Show faces detected in webcam with their expressions'''
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
        '''Check if there is a new reaction and append it to reactions list'''
        if self.new_reaction != self.current_reaction:
            self.current_reaction = self.new_reaction
            running_time = perf_counter() - self.start
            self.reactions.append((self.new_reaction, running_time))

    def check_stop(self, debug_mode):
        '''Check if user wants to stop and save reactions to file'''
        # exitApp = cv2.waitKey(1) & 0xFF == ord(self.exit_character)
        if debug_mode == True:
            exitApp = eel.checkDebugButton()()
        else:
            exitApp = eel.checkRunButton()()
        if exitApp:
            print(f'{self.reactions = }')
            results = pd.DataFrame(self.reactions)
            results.to_excel(f"{path}/Results.xlsx", sheet_name='Detected Expresions')
            return True


def start(debug_mode):
    '''Starts debug mode'''
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
        sleep(0.1)
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
    '''Open the folder containing the results files'''
    subprocess.Popen(f'explorer "{path}"')


eel.start('index.html', size=(520, 235))
