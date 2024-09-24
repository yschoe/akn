#!/usr/bin/python
# mk-abstract-book.py
#
# input: AKN preregistration data : TSV format

import pandas as pd
import copy
import re
import math
import sys
from datetime import datetime
import pytz

# Set the time zone to US Central
central_tz = pytz.timezone('US/Central')

# Get the current time in UTC
utc_now = datetime.utcnow()

# Convert UTC time to US Central Time
central_now = utc_now.replace(tzinfo=pytz.utc).astimezone(central_tz)


if (len(sys.argv) != 2):
  print("usage: ./mk-abstract-book.py <csv-filename>")
  exit()


year = datetime.datetime.now().year

print(year_string)
#--------------------
# CONFIG
#--------------------
#year = 2023 : computed above
filename = sys.argv[1]	
lastname = "Last name (in English: Kim, Lee, Park, etc.)"    # column title for lastname
firstname = "First name (in English)"  # column title for firsname
#--------------------


'''

  functions

'''
def print_header (year):

  print("Updated: ", central_now.strftime('%Y-%m-%d %H:%M:%S %Z'))
  print("<table>")
  print("<tr><td></td><td><b>Name</b></td><td></td> <td><b>Affiliation</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td><b>Abst</b></td> <td> <b>Theme </b></td></tr>")


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

  # 0. Only if all caps
  if len(re.findall("[a-z]",name))>0:
    return name

  dash_loc = name.find('-')

  # 1. two words, and "-" in the middle
  words = re.split('\s|-',name)

  ret = ""
  for w in words:
    ret = ret+w.capitalize()+" "
  ret = ret[:-1]

  # put back dash
  if dash_loc>0:
    ret = ret[:dash_loc] + "-" + ret[dash_loc+1:]

  # 2. parenthesized nicknames
  words = re.split('\(',ret)

  if (len(words)>1):
    ret = ""
    n = 0
    for w in words:
      if n==0:
        ret = ret+w+"("
      else:
        ret = ret+w.capitalize()
      n += 1

  return ret

'''
  
  1. load CSV file 

'''
df = pd.read_csv(filename)
df = df.sort_values(by=[lastname,firstname],ascending=True)

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
  td_print( capitalize(df[lastname][idx]) )
  td_print( capitalize(df[firstname][idx]) )

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
