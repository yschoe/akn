#!/usr/bin/python
# mk-abstract-book.py
#
# input: AKN preregistration data : TSV format

import pandas as pd
import copy
import re
import math
import sys

if (len(sys.argv) != 2):
  print("usage: ./mk-abstract-book.py <csv-filename>")
  exit()

#--------------------
# CONFIG
#--------------------
year = 2022
filename = sys.argv[1]	
lastname = "Last name (in English)"    # column title for lastname
firstname = "First name (in English)"  # column title for firsname
#--------------------


'''

  functions

'''
def print_header (year):

  print("<h3>AKN Abstracts "+str(year)+"</h3>") 
  print("<table>")
  print("<tr><b><td></td><td><b>Name</b></td><td>&nbsp</td> <td><b>Affiliation</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td> <b>Theme </b></td></b></tr>")


def print_footer ():

  print("</tr></table>") 


def td_print (txt):

  print("<td> "+str(txt)+" </td>")


def td_print_url (tag,url):
  
  print('<td> <a href="'+url+'">'+tag+'</a> </td>')


def capitalize (name):
  '''
  quick hack to properly capitalize names
  '''

  words = re.split("\s",name)
  # 1. two words
  ret = ""
  if (len(words)==2):
    for w in words:
       ret = ret+w.capitalize()+" "
    ret = ret[:-1]
  
  words = re.split("-",ret)
  # 2. A-B 
  if (len(words)>1):
    ret = ""
    for w in words:
       ret = ret+w.capitalize()+"-"
    return ret[:-1]

  # 3. Other  
  return name.capitalize()

'''
  
  1. load CSV file 

'''
df = pd.read_csv(filename)
df = df.sort_values(by=['Last name (in English)','First name (in English)'],ascending=True)

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

  td_print(str(n)+'&nbsp;')
  n+=1

  # 1. Name
  td_print( capitalize(df['Last name (in English)'][idx]) )
  td_print( capitalize(df['First name (in English)'][idx]) )

  # 2. Affiliation
  td_print(df['Affiliation'][idx])

  # 3. Abstracts
  for i in range(0,5):
    url = df[abst_cols[i]][idx]
    if (not isinstance(url,str) and math.isnan(url)):
      td_print(' &nbsp; ')
    else:
      if (re.search("abstractsonline",url) and re.search("presentation", url)):
        td_print_url('Abst'+str(i+1),url)
      else:
        td_print_url('invalid url',url)

  # 4. Theme
  td_print(df['Research area'][idx])

  # endline
  print('</tr>')


print_footer()
