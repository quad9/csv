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
import t14i_regex
import t14i_string

# read CSV file
file_paths = glob.glob("./_org/*.csv")

for org_file in file_paths:
    #####################
    # 「ファイル名 + 拡張子」を取得する。
    filename = os.path.basename(org_file)

    # create deta frame of pandas
    df_in = pd.read_csv(org_file, encoding = 'utf-8')

    # 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
    to_tmp_file = os.path.join('./_tmp', filename)    
    df_in.to_csv(to_tmp_file,
        encoding = "utf-8",
        index = False,
        columns=["番号", "曲名", "作曲者", "氏", "名", "担当講師", "演奏楽器"],
        sep = ',')

    df = pd.read_csv(to_tmp_file, encoding='utf-8')


    #####################
    # 同じグループの縦セルをつまんでいくコードのためのインデックス作成
    ###
    # play_anchor_index
    # 処理開始のアンカーとなる配列の作成
    # セルを縦につまむ際のトリガーになるインデックスをdf["番号"]から導き出す。
    play_anchor_index = []
    for i, num in enumerate(df["番号"]):
        if pd.isnull(num):
            continue
        else:
            play_anchor_index.append(i)

    ###
    # pause_anchor_index
    # 処理ここまでと合図するアンカーの配列の作成
    pause_anchor_index = [n - 1 for n in play_anchor_index[1:]]
    pause_anchor_index.append(len(df) - 1)

    ###
    # anchor_index
    anchor_index = []
    for play, pause in zip(play_anchor_index, pause_anchor_index):
        anchor_index.append([play, pause])


    #####################
    # df["演奏者"]
    # df["氏"], df["名"]の整理とdf["演奏者"]の生成
    # 下準備
    columns = [df["氏"], df["名"]]
    column_labels = ["氏", "名"]
    # 整理
    for i, col in enumerate(columns):
        # セルに空白がある場合『〓』で埋める。
        # セル内文字の前後の空白を削除する。
        df[column_labels[i]] = [name.strip() for name in col.fillna("〓〓")]
    # 生成
    df["演奏者"] = [t14i_string.name7justify(name) for name in columns[0] + "　" + columns[1]]

    #####################
    # df["演奏楽器"]
    # df["演奏楽器"]の整理
    # セルに空白がある場合『〓』で埋める。
    df["演奏楽器"] = df["演奏楽器"].fillna("〓")
    tmp_mi = []
    for mi in df["演奏楽器"]:
        mi = re.sub('.*ピアノ.*', 'P', mi)
        mi = re.sub('.*エレクトーン.*', 'E', mi)
        tmp_mi.append(mi)
    df["演奏楽器"] = tmp_mi

    ###############################################################


    #####################
    # df["曲名"]を整理
    tmp_writer = []
    for name in df["曲名"]:
        if name is np.nan:
            tmp_writer.append(np.nan)
        else:
            tmp_writer.append(t14i_regex.re_cellstr(name))
    df["曲名"] = tmp_writer


    #####################
    # df["作曲者"]を整理
    tmp_writer = []
    for name in df["作曲者"]:
        if name is np.nan:
            tmp_writer.append(np.nan)
        else:
            name = t14i_regex.re_cellstr(name)
            if name.isascii():
                tmp_writer.append(name)
            else:
                if "/" in name:
                    writers = "/".join([t14i_string.name4justify(ins) for ins in name.split("/")])
                    tmp_writer.append(writers)
                else:
                    tmp_writer.append(t14i_string.name4justify(name))
    df["作曲者"] = tmp_writer


    #####################
    # df["担当講師"]から氏名の重複をとりユニコード順で氏名を『/』で区切った文字列を生成しておく。
    tmp_teacher = []

    for teacher in df["担当講師"]:
        if teacher is np.nan:
            continue
        else:
            tmp_teacher.append(t14i_string.name4justify(teacher))
    
    # 最終的にdf["担当講師"]の最初の要素として入れる値を文字列で保持する。
    teachers = "/".join(sorted(list(set(tmp_teacher))))


    #####################
    # アンカーを元に同じグループのものを縦につまんでいく。
    # df["演奏者"]
    # NaNで埋めた行分の配列を生成。
    tmp_column = [np.nan] * len(df)
    columns = [df["演奏者"], df["演奏楽器"]]
    column_labels = ["演奏者", "演奏楽器"]
    for index, col in enumerate(columns):
        for i, scope in zip(play_anchor_index, anchor_index):
            tmp_column[i] = "/".join(col[scope[0]: scope[1] + 1])
        df[column_labels[index]] = tmp_column


    #####################
    # CSVに上書きで書き出し

    # 出力ファイル用にコラムを収集して書き出す。
    df_out = df.reindex(columns = ['番号', '曲名', '作曲者', '演奏者', '演奏楽器'])
    

    # セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
    # これらを取り除く処理をする。
    df_out = df_out.dropna(how='all').dropna(how='all', axis = 1)


    #####################
    # df["番号"]、df["人数"]のフロートを整数に変更して整理する。
    df_out["番号"] = df_out["番号"].astype('float').astype('int')


    #####################
    # df_out["担任"]
    # teachersを使ってdf["担任講師"]→df_out["担任"]
    tmp_column = [np.nan] * len(df_out)
    tmp_column[0] = teachers
    df_out["担任"] = tmp_column


    df_out["曲名"] = df_out["曲名"].fillna("〓〓〓〓")
    df_out["作曲者"] = df_out["作曲者"].fillna("〓〓〓〓")


    #####################
    # 成り行きで最後に持ってきた。
    # lib/t14i_regex.csv_reg()に渡してセル内の文字列を整理する。
    df_out = t14i_regex.csv_reg(df_out)


    # CSVとして書き出し
    to_gen_file = os.path.join('./_gen', filename)
    df_out.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['番号', '曲名', '作曲者', '演奏者', '演奏楽器', "担任"],
        sep = ',')


    #####################
    ### オリジナルと中間ファイルを削除する。
    # 検証をするときはこれらを外す。
    os.remove(org_file)
    os.remove(to_tmp_file)