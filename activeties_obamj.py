import os
import glob
import shutil
import jaconv
import re
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。

# 月刊大阪弁護士会　表3「今後の主な行事等」を整理するためのコード

###################
# 下準備
# ファイルは1枚だけが前提。
org_file = glob.glob("./_org/*.csv")[0]
filename = os.path.basename(org_file)
# create deta frame of pandas
df_in = pd.read_csv(org_file, encoding='utf-8')

# 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
to_tmp_file = os.path.join('./_tmp', filename)
df_in.to_csv(to_tmp_file,
    encoding = "utf-8",
    index = False,
    columns=["日時", "時間", "内容", "場所"],
    sep = ',') 
df = pd.read_csv(to_tmp_file, encoding = "utf-8")


# lib/t14ireに渡してセル内の文字列を整理する。<<<<<<<<<<
df = t14i_regex.csv_reg(df_in)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 列の整理。
df['日時'] = '【日時】' + df['日時']
df['日付'] = df['日時'] + df['時間']
df['場所'] = '【場所】' + df['場所']
df['概要'] = df['日付'] + '▼' + df['場所']

# 変更した内容を元のファイルへ上書き保存する。
df.to_csv(file,
          encoding = "utf-8",
          index = False,
          columns = ['内容', '概要'],
          sep = '\t')


# #####################
# neta
# # アンカーを元に同じグループのものを縦につまんでいく。
# # 下準備
# columns = [df["出演者名"], df["作曲者名"], df["編曲者名"], df["会場名"]]
# column_labels = ["出演者名", "作曲者名", "編曲者名", "会場名"]    
# anchor_index = ntzarr.pickcell(df["番号"])
# play_anchor_index = [range[0] for range in anchor_index]
# for index, column in enumerate(columns):
#     # NaNで埋めた行分の配列を生成。
#     container_colunm = [np.nan] * len(df)
#     # anchor_index
#     for i, scope in zip(play_anchor_index, anchor_index):
#         container = []
#         for name in column[scope[0]: scope[1]]:
#             if pd.isnull(name):
#                 continue
#             else:
#                 container.append(name)
#         # 『/』で繋いだ文字列として格納する。
#         container_colunm[i] = "/".join(container)
#     df[column_labels[index]] = container_colunm