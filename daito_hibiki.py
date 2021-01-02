import glob
import jaconv
import re
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。


# read CSV file
file_path = glob.glob("./*.csv")
file = file_path[0]
# create deta frame of pandas
df_in = pd.read_csv(file, encoding = 'utf-8')

# セルごとの文字列クリーニングを先にすると『NaN』が『nan』になり、
# dorpnaメソッドが効かなくなるので、不要なNaN行を先に削除処理する。
df = df_in.dropna(how='all')

# lib/t14ireに渡してセル内の文字列を整理する。
df = ntzreg.csv_reg(df)

# 演者の氏名を揃える
tmp_cell = []
tmp_players = []
for players in df["演者"]:
  for cell_str in players.split("▽"):
    arr = cell_str.split()
    uji = arr[0]
    mei = arr[1]
    uji_size = len(arr[0])
    mei_size = len(arr[1])
    # 〓　　　　　〓
    if uji_size == 1 and mei_size == 1:
      tmp_cell.append(f'{arr[0]}　　　　　{arr[1]}')
    # 〓　〓　〓　〓
    elif uji_size == 2 and mei_size == 2:
      tmp_cell.append(f'{arr[0][0]}　{arr[0][1]}　{arr[1][0]}　{arr[1][1]}')
    # 〓　　　〓　〓
    elif uji_size == 1 and mei_size == 2:
      tmp_cell.append(f'{arr[0]}　　　{arr[1][0]}　{arr[1][1]}')
    # 〓　〓　　　〓
    elif uji_size == 2 and mei_size == 1:
      tmp_cell.append(f'{arr[0][0]}　{arr[0][1]}　　　{arr[1]}')
    # 〓　　　〓〓〓 or 〓〓〓　　　〓
    elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
      tmp_cell.append(f'{arr[0]}　　　{arr[1]}')
    # 〓　〓　〓〓〓
    elif uji_size == 2 and mei_size == 3:
      tmp_cell.append(f'{arr[0][0]}　{arr[0][1]}　{arr[1]}')
    # 〓〓〓　〓　〓
    elif uji_size == 3 and mei_size == 2:
      tmp_cell.append(f'{arr[0]}　{arr[1][0]}　{arr[1][1]}')
    # 〓〓〓　〓〓〓
    elif uji_size == 3 and mei_size == 3:
      tmp_cell.append(f'{arr[0]}　{arr[1]}')
    # 〓〓〓　〓〓〓〓 or 〓〓〓〓　〓〓〓
    elif uji_size == 3 and mei_size == 4 or uji_size == 4 and mei_size == 3:
      tmp_cell.append(f'{arr[0]}{arr[1]}')
    else:
      tmp_cell.append('例外発生')
  tmp_players.append(tmp_cell)
df["演者"] = tmp_players

tmp_arr = []
for arr in df["演者"]:
  joined_arr = "\t".join(arr)
  tmp_arr.append(f"\t{joined_arr}")
df["演者"] = tmp_arr

# 番号を文字列のfloatから整数に変換する。
df['番号'] = df['番号'].astype('float').astype('int')

# 新規でファイルに書き込む。
with open('hibki.txt', 'w') as file:
  for i in range(len(df)):
    file.write(f"{(df['番号'][i])}.{df['曲名'][i]}\n{df['演者'][i]}\n")