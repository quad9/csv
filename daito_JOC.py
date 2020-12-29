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

    # 中間ファイル生成
    # create deta frame of pandas
    df_in = pd.read_csv(org_file, encoding = 'utf-8')

    # 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
    # 『./』現在プログラムファイルがある階層の指示はあってもなくても結果は同じ。
    # 上手く通る。一応付けておく。
    to_tmp_file = os.path.join('./_tmp', filename)
    df_in.to_csv(to_tmp_file,
        encoding = "utf-8",
        index = False,
        columns = ["順番", "曲名", "氏", "名", "コース名", "演奏楽器", "共演者名"],
        sep = ',')

    # 加工するDataFrameの生成
    df = pd.read_csv(to_tmp_file, encoding = 'utf-8')


    #####################
    # df["氏"], df["名"]の整理とdf["出演者"]の生成
    # 下準備
    columns = [df["氏"], df["名"]]
    column_labels = ["氏", "名"]
    # 整理
    for i, col in enumerate(columns):
        # セルに空白がある場合『〓』で埋める。
        col = col.fillna("〓〓")
        # セル内文字の前後の空白を削除する。
        df[column_labels[i]] = [name.strip() for name in col]
    # 生成
    df["出演者名"] = [t14i_string.name7justify(name) for name in columns[0] + "　" + columns[1]]

    
    #####################
    # df["コース名"]の整理
    # セルに空白がある場合『〓』で埋める。
    df["コース名"] = df["コース名"].fillna("〓〓〓〓")
    tmp_course = []
    for course in df["コース名"]:
        course = course.replace('ジュニア専門コース', 'ジュニア専門')
        # pythonでregのあつかいがややこしい印象。
        # （Rubyをかじったせいかreplaceってダサそうに思ってしまう悪い悪癖。）
        # 結局PerlもRubyも中途半端に投げたんやからそこは謙虚にせなあかん。
        # course = re.sub('(ジュニア専門コース)(.+)', r'ジュニア専門\2', course)
        course = re.sub('ジュニア総合|総合ジュニア', 'ジュニア総合コース', course)
        tmp_course.append(course)
    df["コース名"] = tmp_course
    
    
    #####################
    # df["演奏楽器"]を整理
    tmp_mi = []
    for mi in df["演奏楽器"].fillna("〓"):
        mi = jaconv.z2h(mi.upper(), kana=False, ascii=True, digit=False)
        tmp_mi.append(mi)
    df["演奏楽器"] = tmp_mi 


    #####################
    # df["共演者名"]の整理と生成
    for i, value in enumerate(df["共演者名"]):
        if pd.isnull(value):
        # if value is np.nan:
            continue
        else:
            arr = value.split("/")
            df["出演者名"][i] = df["出演者名"][i] + "▼" + t14i_string.name4justify(arr[0])
            df["コース名"][i] = df["コース名"][i] + "▼"
            df["演奏楽器"][i] = df["演奏楽器"][i] + "▼" + arr[1]


    # lib/t14i_regex.csv_reg()に渡してセル内の文字列を整理する。
    df = t14i_regex.csv_reg(df)

    #####################
    ### 出力する。
    to_gen_file = os.path.join('./_gen', filename)
    df.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ["順番", "曲名", "出演者名", "コース名", "演奏楽器"],
        sep = ',')


    #####################
    ### オリジナルと中間ファイルを削除する。
    # 検証をするときはこれらを外す。
    os.remove(org_file)
    os.remove(to_tmp_file)