import os
import glob
import re
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import t14i_regex
import t14i_string

# 月刊大阪弁護士会　新期入会員データを整理するためのコード

##############################
# ### 下準備

# read CSV file
file_path = glob.glob("./*.csv")
file = file_path[0]

# create deta frame of pandas
df = pd.read_csv(file, encoding='utf-8')

# セルごとの文字列クリーニングを先にすると『NaN』が『nan』になり、
# dorpnaメソッドが効かなくなるので、不要なNaN行を先に削除処理する。
# 行のNaN,列のNaNの順番で削除する。
df = df.dropna(how='all').dropna(how='all', axis=1)

# 空欄を「〓〓〓〓」で埋める。
df = df.fillna("〓〓〓〓")

# lib/t14ireに渡してセル内の文字列を整理する。
df = t14i_regex.csv_reg(df)


##############################
# ### df["@写真名"]と写真ファイルのリネーム

# 写真用に氏名を揃える
tmp_names_with_photo = []
for name in df["氏名"]:
    tmp_names_with_photo.append(t14i_string.name5justify(name))
df["写真用氏名"] = tmp_names_with_photo

# 写真ファイルパスを読み込んで下準備
origin_path = sorted(glob.glob("./*.psd"))
tmp_photo_file_names = []
for path in origin_path:
    basename, ext = os.path.splitext(os.path.basename(path))
    tmp_photo_file_names.append(basename)
df["元ファイル名"] = tmp_photo_file_names

# df["@写真名"]の作成
df["@写真名"] = "img" + df["元ファイル名"] + "_" + df["写真用氏名"] + ".psd"

# 設定した写真名をファイルに一括でファイル名を上書きする。
for index in range(len(df)):
    os.rename(origin_path[index], df["@写真名"][index])


##########################
# 氏名にルビを付け ver2
# 氏名のそれぞれの漢字にルビを付与する。
df["氏名ルビ付"] = t14i_string.each_han_with_ruby(df["ふりがな用氏名"], df["ふりがな用"])
print(df["氏名ルビ付"])


##########################
# 氏名にルビを付け ver1
# 条件は、
# 氏名、ふりがな共に『氏 + スペース + 名』で分けているdfであること。
# 　例）青木　克也
# 　　　あおき　かつや

# tmp_df = df["氏名"] + "　" + df["ふりがな"]

# tmp_name_with_ruby = []
# for name in tmp_df:
#   tmp_name_with_ruby.append(t14i_string.name4justify_with_ruby(name))

# df["氏名ルビ付"] = tmp_name_with_ruby


##########################
# df['登録番号']を整数に変換
tmp_nums = []
for index in range(len(df)):
  num = df["登録番号"][index]
  if ".0" in num:
    tmp_nums.append(num.replace(".0", ""))
  else:
    tmp_nums.append(num)

df["登録番号"] = tmp_nums

##########################
# インデザイン・ドキュメント用のフォーマットで氏名を変更する。
tmp_name = []
for name in df["氏名"]:
  tmp_name.append(t14i_string.name4justify(name))

df["氏名"] = tmp_name

##########################
# csvで書き出す。
df.to_csv("新期会員名簿.csv",
          encoding="utf-16",
          index=False,
          columns=("番号", "氏名", "ふりがな", "〒", "事務所住所1", "事務所住所2", "事務所", "TEL", "FAX", "登録番号", "修習地", "氏名ルビ付", "@写真名"),
          sep=',')