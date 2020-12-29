import glob
import jaconv
import re
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import t14i_regex

file_paths = glob.glob("./*.csv")

for file in file_paths:
  df = pd.read_csv(file, encoding = 'utf-8')

  # df["名前"] = df["名前"].replace('([^a-zA-Z]+)[ 　]+([^a-zA-Z]+)', r'\1\2', regex=True)

  tmp_arr = []
  for cell in df["名前"]:
    if re.match('([^a-zA-Z]+)[ 　]+([^a-zA-Z]+)', cell):
      cell = re.sub(r'[ 　]+', '', cell)
    else:
      cell = re.sub(r'[ 　]+', ' ', cell)

    print(cell)
    # tmp_arr.append(cell)

  # df["名前"] = tmp_arr
  # tmp_arr = []
  # for cell in df["名前"]:
  #   cell = re.sub('([^a-zA-Z]+)[ 　]+([^a-zA-Z]+)', r'\1\2', cell)
  #   tmp_arr.append(cell)
  # df["名前"] = tmp_arr


# str = "高      広 　信　　　　　　　　之"
# new_str = re.sub('[ 　]+', '■', str)
# print(new_str)
