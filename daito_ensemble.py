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

# pprintで見やすく表示。
# pprint.pprint(配列)

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
        columns=["番号", "曲名", "作曲者名", "編曲者名", "グループ名", "氏", "名", "人数", "会場名"],
        sep = ',')

    df = pd.read_csv(to_tmp_file, encoding='utf-8')


    #####################
    # 同じグループの縦セルをつまんでいくコードのためのインデックス作成

    ###
    # 『play_anchor_index』
    # 処理開始のアンカーとなる配列の作成
    # セルを縦につまむ際のトリガーになるインデックスをdf["番号"]から導き出す。
    play_anchor_index = []
    for i, num in enumerate(df["番号"]):
        if pd.isnull(num):
            continue
        else:
            play_anchor_index.append(i)

    # 処理ここまでと合図するアンカー生成のための仮アンカー。
    # 最終行のインデックス番号を追加しておく。
    # 全体の長さから1引いた数がそれ。
    tmp_anchor_index = copy.deepcopy(play_anchor_index)
    tmp_anchor_index.append(len(df) - 1)


    # 処理ここまでと合図するアンカーの配列の作成
    pause_index = []
    for i in tmp_anchor_index:
        # 最初と最後のインデックス以外。
        if i > 0 and i != tmp_anchor_index[-1]:
            pause_index.append(i - 1)
        # 最後のインデックスはそのまま挿入。
        elif i != 0:
            pause_index.append(i)
        # 最初のインデックスは不要。
        else:
            continue

    ###
    # 『anchor_index』
    # 配列の要素数が合わなければ会わない分は処理を無視される。
    # だからこの一行は不要。
    # tmp_anchor_index.pop()
    anchor_index = []
    for ta, p in zip(tmp_anchor_index, pause_index):
        anchor_index.append([ta, p])


    #####################
    # df["作曲者名"]を整理
    tmp_writer = []
    for name in df["作曲者名"]:
        if name is np.nan:
            tmp_writer.append(np.nan)
            continue
        else:
            name = name.strip()
            res = re.search("\s", name)
            if res == None:
                tmp_writer.append(name)
            else:
                tmp_writer.append(t14i_string.name4justify(name))
    df["作曲者名"] = tmp_writer


    #####################
    # df["編曲者名"]を整理
    tmp_arrangers = []
    for name in df["編曲者名"]:
        if name is np.nan:
            tmp_arrangers.append(np.nan)
            continue
        else:
            name = name.strip()
            res = re.search("\s", name)
            if res == None:
                tmp_arrangers.append(name)
            else:
                tmp_arrangers.append(t14i_string.name4justify(name))
    df["編曲者名"] = tmp_arrangers


    #####################
    # df["出演者名"]を整理
    df["出演者名"] = df["氏"] + "　" + df["名"]
    tmp_name = [t14i_string.name7justify(name) for name in df["出演者名"]]
    df["出演者名"] = tmp_name


    #####################
    # アンカーを元に同じグループのものを縦につまんでいく。
    ###
    # df["出演者名"]

    # NaNで埋めた行分の配列を生成。
    players = [np.nan] * len(df)
    # dfより、配列で処理した方が今は理解できるのでこうした。
    tmp_players = list(df["出演者名"])
    for i, scope in zip(play_anchor_index, anchor_index):
        # 『/』で繋いだ文字列として格納する。
        players[i] = "/".join(tmp_players[scope[0]:scope[1] + 1])
    df["出演者名"] = players

    ###
    # df["作曲者"]
    # NaNで埋めた行分の配列を生成。
    writers = [np.nan] * len(df)
    # dfより、配列で処理した方が今は理解できるのでこうした。
    tmp_writers = list(df["作曲者名"])
    for i, scope in zip(play_anchor_index, anchor_index):
        name_arr = []
        for name in tmp_writers[scope[0]:scope[1] + 1]:
            if pd.isnull(name):
                continue
            else:
                name_arr.append(name)
        writers[i] = "/".join(name_arr)
    df["作曲者名"] = writers
    
    ###
    # df["編曲者"]
    # NaNで埋めた行分の配列を生成。
    arrangers = [np.nan] * len(df)
    # dfより、配列で処理した方が今は理解できるのでこうした。
    tmp_arrangers = list(df["編曲者名"])
    for i, scope in zip(play_anchor_index, anchor_index):
        name_arr = []
        for name in tmp_arrangers[scope[0]:scope[1] + 1]:
            if pd.isnull(name):
                continue
            else:
                name_arr.append(name)
        arrangers[i] = "/".join(name_arr)
    df["編曲者名"] = arrangers

    ###
    # df["会場名"]
    # NaNで埋めた行分の配列を生成。
    place = [np.nan] * len(df)
    # dfより、配列で処理した方が今は理解できるのでこうした。
    tmp_place = list(df["会場名"])
    for i, scope in zip(play_anchor_index, anchor_index):
        name_arr = []
        for name in tmp_place[scope[0]:scope[1] + 1]:
            if pd.isnull(name):
                continue
            else:
                name_arr.append(name)
        place[i] = "/".join(name_arr)
    df["会場名"] = place


    #####################
    # CSVに上書きで書き出し

    # 出力ファイル用にコラムを収集して書き出す。
    df_out = df.reindex(columns = ['番号', '曲名', '作曲者名', '編曲者名', 'グループ名', '出演者名', '人数', '会場名'])

    # セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
    # これらを取り除く処理をする。
    df_out = df_out.dropna(how='all').dropna(how='all', axis = 1)

    #####################
    # df["番号"]、df["人数"]のフロートを整数に変更して整理する。
    df_out["番号"] = df_out["番号"].astype('float').astype('int')
    df_out["人数"] = df_out["人数"].astype('float').astype('int')


    #####################
    # 成り行きで最後に持ってきた。
    # lib/t14i_regex.csv_reg()に渡してセル内の文字列を整理する。
    df_out = t14i_regex.csv_reg(df_out)


    #####################
    # CSVとして書き出し
    to_gen_file = os.path.join('./_gen', filename)
    df_out.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ['番号', '曲名', '作曲者名', '編曲者名', 'グループ名', '出演者名', '人数', '会場名'],
        sep = ',')

    
    #####################
    ### オリジナルと中間ファイルを削除する。
    # 検証をするときはこれらを外す。
    os.remove(org_file)
    os.remove(to_tmp_file)