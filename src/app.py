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
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import openpyxl
import numpy

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
            self.translate_reactions()
            self.create_step_reactions_list()
            self.create_frequency_list()
            self.save_to_excel()
            print(f'\n{self.reactions = }')
            print(f'\n{self.reactions_step = }')
            print(f'\n{self.sorted_frequency_list = }')
            # results = pd.DataFrame(self.reactions)
            # results.to_excel(f"{path}/Results.xlsx", sheet_name='Expressões detectadas')
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

    def translate_reactions(self):
        '''Traduz lista de reações'''

        for index, reaction in enumerate(self.reactions):
            item = list(reaction)
            match item[0]:
                case 'neutral':
                    item[0] = 'neutro'
                case 'happy':
                    item[0] = 'feliz'
                case 'fear':
                    item[0] = 'medo'
                case 'angry':
                    item[0] = 'raiva'
                case 'sad':
                    item[0] = 'triste'
                case 'disgust':
                    item[0] = 'desgosto'
                case 'surprise':
                    item[0] = 'surpresa'
            self.reactions[index] = tuple(item)

    def save_to_excel(self):
        '''Gera gráficos e salva junto com dados em Excel'''

        df1 = pd.DataFrame(self.reactions_step)
        x1 = df1[1]
        y1 = df1[0]
        df2 = pd.DataFrame(self.sorted_frequency_list)
        x2 = df2[0]
        y2 = df2[1]

        fig = plt.figure()
        fig = plt.figure(figsize=(len(self.reactions_step)/6, 5))
        ax = fig.gca()
        plt.plot(x1, y1, linewidth=2, markersize=1)
        plt.ylabel('Reação', fontweight='bold')
        plt.xlabel('Tempo [s]', fontweight='bold')
        ax.set_xticks(numpy.arange(0, self.reactions_step[-1][1]+2, 2))
        plt.grid(linestyle=':')
        plt.tight_layout()
        plt.savefig("GraficoLinhas.png")
        plt.clf()

        plt.figure()
        plt.bar(x2, y2)
        plt.xlabel('Reação', fontweight='bold')
        plt.ylabel('Tempo [s]', fontweight='bold')
        for i in range(len(x2)):
            plt.text(i, y2[i], y2[i], ha='center')
        plt.tight_layout()
        plt.savefig("GraficoBarras.png")
        plt.clf()

        wb = openpyxl.Workbook()

        sheet = wb.active
        sheet.title = "Emoções por segundo"
        sheet.cell(1, 1).value = "REAÇÃO"
        sheet.cell(1, 2).value = "TEMPO [s]"
        for item in self.reactions_step:
            sheet.append(item)
        grafico_linhas = openpyxl.drawing.image.Image("GraficoLinhas.png")
        grafico_linhas.anchor = 'D1'
        sheet.add_image(grafico_linhas)

        sheet = wb.create_sheet()
        sheet.title = 'Ranking de reações'
        sheet.cell(1, 1).value = "REAÇÃO"
        sheet.cell(1, 2).value = "TEMPO [s]"
        for item in self.sorted_frequency_list:
            sheet.append(item)
        grafico_barras = openpyxl.drawing.image.Image("GraficoBarras.png")
        grafico_barras.anchor = 'D1'
        sheet.add_image(grafico_barras)

        wb.save(f"{path}/Results.xlsx")
        wb.close

        os.remove("GraficoLinhas.png")
        os.remove("GraficoBarras.png")


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
