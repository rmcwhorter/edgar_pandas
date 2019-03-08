import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import consolidated_storage as cs

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

html_table = cs.cashflows

# fix HTML
soup = BeautifulSoup(html_table, "html.parser")
for body in soup("tbody"):
    body.unwrap()

df = pd.read_html(str(soup), flavor="bs4")
df[0] = df[0].drop(columns=[1,2,5,6])

cols = [3,4]
'''
for a in df[0].index:
    print(df[0][a])
'''



df[0].to_excel("cashflows.xlsx")
print(df[0].columns.values)
print(df[0])