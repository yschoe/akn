#!/usr/bin/python
# mk-abstract-book.py
#
# input: AKN preregistration data : TSV format

import pandas as pd
import copy
import re
import math

# CONFIG
year = 2022
filename = '2018.csv'


'''

  functions

'''
def print_header (year):

  print("<h3>AKN Abstracts "+str(year)+"</h3>") 
  print("<table>")
  print("<tr><b><td></td><td><b>Name</b></td> <td><b>Affiliation</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td> <b>Theme </b></td></b></tr>")


def print_footer ():

  print("</tr></table>") 


def td_print (txt):

  print("<td> "+str(txt)+" </td>")


def td_print_url (tag,url):
  
  print('<td> <a href="'+url+'">'+tag+'</a> </td>')


'''
  
  1. load CSV file 

'''
df = pd.read_csv(filename)
df = df.sort_values(by=['Lastname','Firstname'],ascending=True)

'''

  2. get header for abstract columns 

'''

cols = df.columns
abst_cols = copy.deepcopy(cols)
abst_cols = abst_cols.tolist()

for c in cols:
  if (not re.search("bstract",c)):
    abst_cols.remove(c)

print_header(year)
 
'''

  3. print name, affiliation, and abstracts 

'''
n = 1
for idx in df.index:

  print('<tr>')

  td_print(n)
  n+=1

  # 1. Name
  td_print(df['Lastname'][idx].capitalize())
  td_print(df['Firstname'][idx].capitalize())

  # 2. Affiliation
  td_print(df['Affiliation'][idx])

  # 3. Abstracts
  for i in range(0,5):
    url = df[abst_cols[i]][idx]
    if (not isinstance(url,str) and math.isnan(url)):
      td_print(' &nbsp; ')
    else:
      if (re.search("abstractsonline",url) and re.search("presentation", url)):
        td_print_url('Abst'+str(i),url)
      else:
        td_print_url('invalid url',url)

  # 4. Theme
  td_print(df['Research area'][idx])

  # endline
  print('</tr>')


print_footer()
