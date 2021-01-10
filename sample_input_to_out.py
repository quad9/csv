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

##### 入力から出力までの流れのサンプル。

###################
# 下準備
# ファイルは1枚だけが前提。
org_file = glob.glob("./_org/*.csv")[0]
filename = os.path.basename(org_file)
# create deta frame of pandas
df_in = pd.read_csv(org_file, encoding='utf-8')

# 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
path_to_tmp_file = os.path.join('./_tmp', filename)
df_in.to_csv(path_to_tmp_file,
    encoding = "utf-8",
    index = False,
    columns=["日時", "時間", "内容", "場所", "備考"],
    sep = ',') 
df = pd.read_csv(path_to_tmp_file, encoding = "utf-8")

#########################################################################
# df_in => df => df_outという流れにしたい場合。
# fillnaしたかっtり、空行、空列を削除するなど出力前に整理整頓をしたい場合に有効と
# 考えて今はこの流れにしている。
# サンプルとして、daito_valentine_concert.pyの後半を参照のこと。
# 将来書く力が付いたら、この流れは再検討する。

# 出力ファイル用にコラムを収集して書き出す。
df_out = df.reindex(columns = ["日時", "時間", "内容", "場所"])
# df_out = df.reindex(columns = ["内容", "概要"])

# セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
# これらを取り除く処理をする。
df_out = df_out.dropna(how='all').dropna(how='all', axis = 1)
#########################################################################

# CSVとして書き出し
to_gen_file = os.path.join('./_gen', filename)
df_out.to_csv(to_gen_file,
    encoding = "utf-8",
    index = False,
    columns = ["日時", "時間", "内容", "場所"],
    sep = ',')


# 行を順に表示させる。
# つまり行ごとの配列を操作するきっかけを作る。
# for i in range(len(df)):
#     print(df.loc[i])
# print(df.loc[0])