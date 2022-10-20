import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as pltline
from openpyxl import load_workbook
import openpyxl
import os

path = f'{os.path.dirname(os.path.realpath(__file__))}\Results'

reactions = [
    ('neutral', 0),
    ('happy', 1.744248399976641),
    ('sad', 2.0440329000120983),
    ('fear', 2.373049699992407),
    ('sad', 2.75135879998561),
    ('neutral', 3.3799759999965318),
    ('sad', 3.6899851000052877),
    ('neutral', 4.007389399979729),
    ('sad', 4.617331699992064)]

df = pd.DataFrame(reactions)

# plt.figure(figsize=(9, 6))
# plt.bar(x=df[0],
#         height=df[1]
#         )
# plt.xticks(rotation=45)
# plt.title("Gráfico", fontsize=25, fontweight='bold')
# plt.xlabel('Reação')
# plt.ylabel('Tempo')

x = df[0]

pltline.figure()
pltline.stairs(x, fill=True)
pltline.title("Gráfico", fontsize=25, fontweight='bold')
pltline.ylabel('Reação')
pltline.xlabel('Tempo')
pltline.show()

# pltline.plot(x, y, 'go--', linewidth=2, markersize=12)
# pltline.title("Gráfico", fontsize=25, fontweight='bold')
# pltline.ylabel('Reação')
# pltline.xlabel('Tempo')
# img = pltline.savefig(f"{path}/GraficoLinha.png")

# wsnew = load_workbook(f"{path}/Results.xlsx")
# newsheet = wsnew.create_sheet("Gráfico", 2)
# img1 = openpyxl.drawing.image.Image(f"{path}/GraficoLinha.png")
# img1.anchor = 'A1'
# newsheet.add_image(img1)
# wsnew.save(f"{path}/Results.xlsx")
# wsnew.close()
