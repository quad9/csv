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
import ntzarr
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
path_to_tmp_file = os.path.join('./_tmp', filename)
df_in.to_csv(path_to_tmp_file,
    encoding = "utf-8",
    index = False,
    columns=["日時", "時間", "内容", "場所", "備考"],
    sep = ',') 
df = pd.read_csv(path_to_tmp_file, encoding = "utf-8")


###################
# アンカーを元に同じグループのものを縦につまんでいく。

# 下準備
# アンカー生成
# アンカーにする『df column』から生成する。
anchor_index = ntzarr.pickcell(df["日時"])
collect_index = [range[0] for range in anchor_index]

for col_name in df.columns:
    # 下準備
    # セル内の文字列を正規表現で整理する。
    for cell in df[col_name]:
        if cell is np.nan:
            continue
        else:
            cell = ntzreg.cellstr(cell, "zs")
    # 時間、場所と備考の処理の分けたいので真偽値を備えておく。
    res = re.search("時間|場所", col_name)
    # 処理開始
    if "日時" in col_name:
        continue
    else:
        # 内容に空欄がある場合は下駄で埋める。
        if "内容" in col_name:
            df[col_name] = df[col_name].fillna("〓〓〓〓〓〓〓〓")
        # 空のコラムを作っておく。
        tmp_empty_col = [np.nan] * len(df)
        # columnの範囲ごとに処理をする。
        # 内容に空欄がある場合は『/（仮の強制改行コード）』で埋める。
        for ci, scope in zip(collect_index, anchor_index):
            scope_container = []
            for i, content in enumerate(df[col_name][scope[0]: scope[1]]):
                if pd.isnull(content):
                    if res == None:
                        scope_container.append("/")
                    else:
                        ##### 空欄は同上の場合、上の欄の値をコピペする仕組み。
                        # columnのインデックス番号を知りたい。
                        # collect_indexから導き出されるscope[0]から何番目というのが
                        # わかると、その前が欲しい値ということ。
                        # scope[0] + i - 1
                        scope_container.append(df[col_name][ scope[0] + i - 1 ])
                else:
                    scope_container.append(content)
            # つまみたいコラムへ内容をペーストする。
            tmp_empty_col[ci] = "/".join(scope_container)
    df[col_name] = tmp_empty_col

# セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
# これらを取り除く処理をする。
df = df.dropna(how='all').dropna(how='all', axis = 1)


# 列の整理。
# df['日時'] = '【日時】' + df['日時']
# df['日付'] = df['日時'] + df['時間']
# df['場所'] = '【場所】' + df['場所']
# df['概要'] = df['日付'] + '▼' + df['場所']


#########################################################################
# df_in => df => df_outという流れにしたい場合。
# fillnaしたかっtり、空行、空列を削除するなど出力前に整理整頓をしたい場合に有効と
# 考えて今はこの流れにしている。
# サンプルとして、daito_valentine_concert.pyの後半を参照のこと。
# 将来書く力が付いたら、この流れは再検討する。

# 出力ファイル用にコラムを収集して書き出す。
df_out = df.reindex(columns = ["日時", "時間", "内容", "場所", "備考"])
# df_out = df.reindex(columns = ["内容", "概要"])

# セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
# これらを取り除く処理をする。
# df_out = df_out.dropna(how='all').dropna(how='all', axis = 1)
#########################################################################

# CSVとして書き出し
to_gen_file = os.path.join('./_gen', filename)
df_out.to_csv(to_gen_file,
    encoding = "utf-8",
    index = False,
    columns = ["日時", "時間", "内容", "場所", "備考"],
    sep = '\t')