import pandas as pd
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import openpyxl
import os
import numpy
from Data import *

cnt = 0


def gera_pontos_linhas(rs1, rs2, rs3, rs4, rs5):
    df1 = pd.DataFrame(rs1)
    df2 = pd.DataFrame(rs2)
    df3 = pd.DataFrame(rs3)
    df4 = pd.DataFrame(rs4)
    df5 = pd.DataFrame(rs5)

    x1 = df1[1]
    y1 = df1[0]
    y2 = df2[0]
    y3 = df3[0]
    y4 = df4[0]
    y5 = df5[0]

    return x1, y1, y2, y3, y4, y5


def gera_grafico_linhas(x1, y1, y2, y3, y4, y5):
    # width = 5 if len(x1)/10 < 5 else len(x1)/10
    fig = plt.figure(figsize=(8, 5))

    ax = fig.gca()

    plt.plot(x1, y1, linewidth=1, marker=".", markersize=4, label="Voluntário A")
    plt.plot(x1, y2, linewidth=1, marker=".", markersize=4, label="Voluntário B")
    plt.plot(x1, y3, linewidth=1, marker=".", markersize=4, label="Voluntário C")
    plt.plot(x1, y4, linewidth=1, marker=".", markersize=4, label="Voluntário D")
    plt.plot(x1, y5, linewidth=1, marker=".", markersize=4, label="Voluntário E")
    plt.ylabel('Reação', fontweight='bold')
    plt.xlabel('Tempo [s]', fontweight='bold')
    plt.yticks([0, 1, 2, 3, 4, 5], ["triste", "raiva", "neutro", "feliz", "medo", "surpresa"
                                    ])
    ax.set_xticks(numpy.arange(0, len(x1), 20))
    plt.grid(linestyle=':')
    plt.tight_layout()
    plt.legend()
    global cnt
    cnt += 1
    plt.savefig("GraficoLinhas_v" + str(cnt) + ".png")
    plt.show()
    plt.clf()


################################ LISTA1 #################################

# x1, y1, y2, y3, y4, y5 = gera_pontos_linhas(rs_1_1, rs_1_2, rs_1_3, rs_1_4, rs_1_5)
# gera_grafico_linhas(x1, y1, y2, y3, y4, y5)

x1, y1, y2, y3, y4, y5 = gera_pontos_linhas(rs_2_1, rs_2_2, rs_2_3, rs_2_4, rs_2_5)
gera_grafico_linhas(x1, y1, y2, y3, y4, y5)

# x1, y1, y2, y3, y4, y5 = gera_pontos_linhas(rs_3_1, rs_3_2, rs_3_3, rs_3_4, rs_3_5)
# gera_grafico_linhas(x1, y1, y2, y3, y4, y5)
