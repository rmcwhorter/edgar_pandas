print("SOF")
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import consolidated_storage as cs
import re

pd.set_option('display.max_columns', 9)

def cashflow_html_to_pandas(html_table):
    # fix HTML
    soup = BeautifulSoup(html_table, "html.parser")
    for body in soup("tbody"):
        body.unwrap()
    
    df = pd.read_html(str(soup), flavor="bs4")[0]

    #This drops any columns in the dataframe that contain only one unique value
    #This helps standardize dataframes   
    #We also want to drop all rows that contain only one unique value
    df_empty_cleaner(df)
    
    #So the first two rows seem always to contain dating information
    #So lets take these and store them somewhere else, then drop them from the table
    dating_information = df.loc[df.index.values[0:2],:]
    print(dating_information)
    df.drop(df.index.values[0:2], inplace=True)
    
    #Remove all instances of '$' from dataframe
    df.replace(to_replace="$", value=np.nan, inplace=True)
    df.replace(to_replace="—", value=0, inplace=True)
    df.replace(to_replace=",", value="", inplace=True)
    df.replace(to_replace="(", value="-", inplace=True)
    
    df_empty_cleaner(df)
    
    return df

def df_empty_cleaner(df):
    for a in df:
        if(len(df[a].unique()) == 1):
            #drop the column
            df.drop(columns=[a], inplace=True)
    
    for index, row in df.iterrows():
        if(len(row.unique()) == 1):
            df.drop(index, inplace=True)
    return df
    
        
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
tsla_in = cs.cashflows_tsla
tsla_out = "cashflows_tsla_raw.xlsx"

aapl_in = cs.cashflows_aapl
aapl_out = "cashflows_aapl_raw.xlsx"

tsla = cashflow_html_to_pandas(tsla_in)
aapl = cashflow_html_to_pandas(aapl_in)

tsla.to_excel(tsla_out)
aapl.to_excel(aapl_out)

print("EOF")