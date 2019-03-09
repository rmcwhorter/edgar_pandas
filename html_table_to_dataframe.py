import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import consolidated_storage as cs
import re

pd.set_option('display.max_columns', 9)

html_table = '''
<table>
  <thead>
    <tr><th>Col1</th><th>Col2</th>
  </thead>
  <tbody>
    <tr><td>1a</td><td>2a</td></tr>
  </tbody>
  <tbody>
    <tr><td>1b</td><td>2b</td></tr>
  </tbody>
</table>'''

html_table = cs.cashflows_tsla

# fix HTML
soup = BeautifulSoup(html_table, "html.parser")
for body in soup("tbody"):
    body.unwrap()

df = pd.read_html(str(soup), flavor="bs4")

#This drops any columns in the dataframe that contain only one unique value
#This helps standardize dataframes
for a in df[0]:
    if(len(df[0][a].unique()) == 1):
        #drop the column
        df[0] = df[0].drop(columns=[a])
    
#We also want to drop all rows that contain only one unique value
for index, row in df[0].iterrows():
    if(len(row.unique()) == 1):
        df[0].drop(index, inplace=True)    
    
        
'''
for a in range(len(df[0].index.values)):
    if(df[0][3][a] != np.nan and df[0][4][a] != np.nan):
        df[0][3][a] = str(df[0][3][a]) + str(df[0][4][a])
    if(df[0][7][a] != np.nan and df[0][8][a] != np.nan):
        df[0][7][a] = str(df[0][7][a]) + str(df[0][8][a])

for a in range(len(df[0].index.values)):
    #Regex to match accounting negative values.... (12345) -> -12345
    #[(][0123456789]*[)]
    
    #remove np.nan s from the data
    df[0][3][a] = df[0][3][a].replace("nan", "")
    df[0][3][a] = df[0][3][a].replace(",", "")
    df[0][3][a] = df[0][3][a].replace("—", "")
    df[0][3][a] = df[0][3][a].replace("(", "-")
    df[0][3][a] = df[0][3][a].replace(")", "")
    
    
    df[0][7][a] = df[0][7][a].replace("nan", "")
    df[0][7][a] = df[0][7][a].replace(",", "")
    df[0][7][a] = df[0][7][a].replace("—", "")
    df[0][7][a] = df[0][7][a].replace("(", "-")
    df[0][7][a] = df[0][7][a].replace(")", "")
    
    try:
        s_three = float(df[0][3][a])
    except:
        print("Threw error trying to convert ", df[0][3][a], " from string to float")
    else:
        df[0][3][a] = s_three
        
    try:
        s_seven = float(df[0][7][a])
    except:
        print("Threw error trying to convert ", df[0][7][a], " from string to float")
    else:
        df[0][7][a] = s_seven

df[0] = df[0].drop(columns=[1,2,4,5,6,8])
'''

df[0].to_excel("cashflows_tsla_raw.xlsx")
print(df[0].columns.values)
print(df[0])