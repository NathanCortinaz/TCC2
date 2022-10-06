import pandas as pd
import os
from pandas.util.testing import makeTimeSeries

df = makeTimeSeries()
df.head()

path = f'{os.path.dirname(os.path.realpath(__file__))}\Results'

df.to_excel(f"{path}/teste.xlsx", sheet_name='Detected Expresions')

print(df)
