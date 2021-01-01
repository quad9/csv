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
import t14i_regex
import t14i_string

# インデックスは、"番号", "氏名", "学年", "作曲者名・編曲者名", "演奏曲名"

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
    columns=["番号", "出演者名", "学年", "作曲者名", "編曲者名1", "編曲者名2", "演奏曲名"],
    sep = ',')

df = pd.read_csv(to_tmp_file, encoding='utf-8')


#####################
# df["氏名"]を生成
# df["出演者名"]をつぶして『本人』と置き換えるための元ネタになるDFを生成する。
df["氏名"] = [t14i_string.name4justify(name) for name in df["出演者名"]]


#####################
# df["作曲者名"], df["編曲者名1"], df["編曲者名2"]を整理する。
columns = [df["作曲者名"], df["編曲者名1"], df["編曲者名2"]]
column_labels = ["作曲者名", "編曲者名1", "編曲者名2"]

for index, col in enumerate(columns):
    tmp_column = []
    for i, name in enumerate(col):
        if name is np.nan:
            tmp_column.append(np.nan)
        else:
            # 文字列の正規化を最初にしておく。
            name = t14i_regex.re_cellstr(name)
            # 1セルに複数名の場合の処理
            if "/" in name:
                tmp_names = []
                for shimei in name.split("/"):
                    shimei = shimei.strip()
                    if shimei.isascii():
                        tmp_names.append(shimei)
                    else:
                        res = re.search("\s", shimei)
                        if res == None:
                            if "本人" in shimei:
                                tmp_names.append(df['氏名'][i])
                            else:
                                tmp_names.append(shimei)
                        else:
                            tmp_names.append(t14i_string.name4justify(shimei))
                tmp_column.append("/".join(tmp_names))
            # 1セルに1名の場合の処理
            else:
                name = name.strip()
                if "本人" in name:
                    tmp_column.append(df["氏名"][i])
                else:
                    if name.isascii():
                        tmp_column.append(name)
                    else:
                        tmp_column.append(t14i_string.name4justify(name))

    df[column_labels[index]] = tmp_column


###################
# df["編曲者名"]の生成
# df["編曲者名1"]とdf["編曲者名2"]をまとめる。
tmp_arrangers = []
for i, arrenger in enumerate(df["編曲者名1"]):
    if df["編曲者名2"][i] is np.nan:
        tmp_arrangers.append(arrenger)
    else:
        tmp_arrangers.append(arrenger + "/" + df["編曲者名2"][i])
df["編曲者名"] = tmp_arrangers


###################
# df["作曲者名・編曲者名"]の生成
df["作曲者名・編曲者名"] = df["作曲者名"] + "▼" + df["編曲者名"].fillna("〓〓〓〓")


#####################
# df["番号"]、df["人数"]のフロートを整数に変更して整理する。
df["番号"] = df["番号"].astype('float').astype('int')


###################
# df["出演者名"]整理
# df["出演者名"]を7文字揃えにする。
df["出演者名"] = [t14i_string.name7justify(player) for player in df["出演者名"]]


###################
# df["学年"]整理
# 学年を整理する。小学校・中学校・高校をとる。
tmp_grade = []
for grade in df["学年"]:
    res = re.search("\d", grade)
    if res == None:
        tmp_grade.append(grade)
    else:
        tmp_grade.append(grade[-2:])
df["学年"] = tmp_grade


###################
# df["演奏曲名"]整理
df["演奏曲名"] = [t14i_regex.re_cellstr(title) for title in df["演奏曲名"]]


###################
# CSVに上書きで書き出し完成
to_gen_file = os.path.join('./_gen', filename)
df.to_csv(to_gen_file,
    encoding = "utf-8",
    index = False,
    columns=["番号", "出演者名", "学年", "作曲者名・編曲者名", "演奏曲名"],
    sep = '\t')


#####################
### オリジナルと中間ファイルを削除する。
# 検証をするときはこれらを外す。
os.remove(org_file)
os.remove(to_tmp_file)