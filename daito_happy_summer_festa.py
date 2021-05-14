import os
import glob
import copy
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
import ntzarr
# from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。


# read CSV file
file_paths = glob.glob("./_org/*.csv")

for org_file in file_paths:
    #####################
    # 「ファイル名 + 拡張子」を取得し変数filenameに格納する。
    filename = os.path.basename(org_file)

    # create deta frame of pandas
    df_in = pd.read_csv(org_file, encoding = 'utf-8')
    # 意図していないNaNを削除して整理する。
    df_in = df_in.dropna(how='all').dropna(how='all', axis = 1)

    # 制作用の中間ファイルを生成。改めてDFを生成して作業の開始。
    # ファイルのパスを生成する。
    to_tmp_file = os.path.join('./_tmp', filename)

    # 中間ファイルを生成する。
    df_in.to_csv(to_tmp_file,
        encoding = "utf-8",
        index = False,
        columns=["氏", "名", "出席"],
        sep = ',')

    # 不要な行列を削除したcsvから本番作業用をDF生成。
    # ここから内容を編集していく。
    # つまり、インスタンスを編集していくイメージ
    df = pd.read_csv(to_tmp_file, encoding='utf-8')

#     #####################
#     # df["作曲者"], df["編曲者名"]を整理
#     columns = [df["作曲者名"], df["編曲者名"]]
#     column_labels = ["作曲者名", "編曲者名"]
#     for index, col in enumerate(columns):
#         tmp_column = []
#         for name in col:
#             if name is np.nan:
#                 tmp_column.append(np.nan)
#             else:
#                 # 文字列の正規化を最初にしておく。
#                 name = ntzreg.cellstr(name)
#                 # 1セルに複数名の場合の処理
#                 if "/" in name:
#                     tmp_names = []
#                     for shimei in name.split("/"):
#                         shimei = shimei.strip()
#                         if shimei.isascii():
#                             tmp_names.append(shimei)
#                         else:
#                             res = re.search("\s", shimei)
#                             if res == None:
#                                 tmp_names.append(shimei)
#                             else:
#                                 tmp_names.append(ntzstr.name4justify(shimei))
#                     tmp_column.append("/".join(tmp_names))
#                 # 1セルに1名の場合の処理
#                 else:
#                     name = name.strip()
#                     if name.isascii():
#                         tmp_column.append(name)
#                     else:
#                         tmp_column.append(ntzstr.name4justify(name))
#         # 生成
#         df[column_labels[index]] = tmp_column


#     #####################
#     # df["出演者名"]
#     # df["氏"], df["名"]の整理とdf["出演者名"]の生成
#     # 下準備
#     columns = [df["氏"], df["名"]]
#     column_labels = ["氏", "名"]
#     # 整理
#     for i, col in enumerate(columns):
#         tmp_col = [ntzreg.cellstr(n) for n in col.fillna("〓〓")]
#         # セルに空白がある場合『〓』で埋める。
#         # セル内文字の前後の空白を削除する。
#         df[column_labels[i]] = [name for name in tmp_col]
#     # 生成
#     df["出演者名"] = [ntzstr.name7justify(name) for name in columns[0] + "　" + columns[1]]


#     #####################
#     # アンカーを元に同じグループのものを縦につまんでいく。
#     # 下準備
#     columns = [df["出演者名"], df["作曲者名"], df["編曲者名"], df["会場名"]]
#     column_labels = ["出演者名", "作曲者名", "編曲者名", "会場名"]    
#     anchor_index = ntzarr.pickcell(df["番号"])
#     play_anchor_index = [range[0] for range in anchor_index]
#     for index, column in enumerate(columns):
#         # NaNで埋めた行分の配列を生成。
#         container_colunm = [np.nan] * len(df)
#         # anchor_index
#         for i, scope in zip(play_anchor_index, anchor_index):
#             container = []
#             for name in column[scope[0]: scope[1]]:
#                 if pd.isnull(name):
#                     continue
#                 else:
#                     container.append(name)
#             # 『/』で繋いだ文字列として格納する。
#             container_colunm[i] = "/".join(container)
#         df[column_labels[index]] = container_colunm


#     #####################
#     # CSVに上書きで書き出し

#     # 出力ファイル用にコラムを収集して書き出す。
#     df_out = df.reindex(columns = ['番号', '曲名', '作曲者名', '編曲者名', 'グループ名', '出演者名', '人数', '会場名'])

#     # セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
#     # これらを取り除く処理をする。
#     df_out = df_out.dropna(how='all').dropna(how='all', axis = 1)


#     #####################
#     # df["番号"]、df["人数"]のフロートを整数に変更して整理する。
#     df_out["番号"] = df_out["番号"].astype('float').astype('int')
#     df_out["人数"] = df_out["人数"].astype('float').astype('int')


#     #####################
#     # 成り行きで最後に持ってきた。
#     # lib/ntzreg.csv_reg()に渡してセル内の文字列を整理する。
#     df_out = ntzreg.csv_reg(df_out)


#     #####################
#     # CSVとして書き出し
#     to_gen_file = os.path.join('./_gen', filename)
#     df_out.to_csv(to_gen_file,
#         encoding = "utf-8",
#         index = False,
#         columns = ['番号', '曲名', '作曲者名', '編曲者名', 'グループ名', '出演者名', '人数', '会場名'],
#         sep = ',')

    
#     #####################
#     ### オリジナルと中間ファイルを削除する。
#     # 検証をするときはこれらを外す。
#     # os.remove(org_file)
#     # os.remove(to_tmp_file)

# # pprintで見やすく表示。
# # pprint.pprint(配列)