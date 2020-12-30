import glob
import jaconv
import re
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import t14i_regex
import t14i_string

# インデックスは、"番号", "曲名", "作曲者", "氏", "名", "演奏楽器"

# read CSV file
file_path = glob.glob("./*.csv")
file = file_path[0]
# create deta frame of pandas
df = pd.read_csv(file, encoding = 'utf-8')

# セルごとの文字列クリーニングを先にすると『NaN』が『nan』になり、
# dorpnaメソッドが効かなくなるので、不要なNaN行を先に削除処理する。
# 行のNaN,列のNaNの順番で削除する。
df = df.dropna(how='all').dropna(how='all', axis = 1)

# # lib/t14ireに渡してセル内の文字列を整理する。
df = t14i_regex.csv_reg(df)

# print(df["演奏者"])

# 演奏者の氏名を揃える
players = []
for player in df["演奏者"]:
  # 1cellに複数行の場合
  if "▽" in player:
    tmp_arr = []
    for str in player.split("▽"):
      tmp_arr.append(t14i_string.name7justify(str))
    players.append("▽".join(tmp_arr))
  # 1cellに1名の場合
  else:
    players.append(t14i_string.name7justify(player))

df["演奏者"] = players

# 番号を文字列のfloatから整数に変換する。
df['番号'] = df['番号'].astype('float').astype('int')

# CSVに上書きで書き出し
df.to_csv(file,
          encoding="utf-8",
          index=False,
          columns=["番号", "曲名", "作曲者", "演奏者", "演奏楽器"],
          sep='\t')
