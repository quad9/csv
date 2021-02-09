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
    # 「ファイル名 + 拡張子」を取得する。
    filename = os.path.basename(org_file)

    # create deta frame of pandas
    df_in = pd.read_csv(org_file, encoding = 'utf-8')

    # 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
    to_tmp_file = os.path.join('./_tmp', filename)    
    df_in.to_csv(to_tmp_file,
        encoding = "utf-8",
        index = False,
        columns=["番号", "曲", "名前", "楽器"],
        sep = ',')

    df = pd.read_csv(to_tmp_file, encoding='utf-8')

    ########## セル内の文字列を正規表現で整形
    # セル内が空欄の時に起こるエラー　int, floatが『elif cell is np.nan:』の
    # 条件分岐で上手く作用してくれないので、『if isinstance(cell, 性質):』で解決している。
    for label in df.columns:
        tmp_df = []
        for cell in df[label]:
            if isinstance(cell, float):
                tmp_df.append(cell)
            elif isinstance(cell, int):
                tmp_df.append(cell)
            elif cell is np.nan:
                tmp_df.append(cell)
            else:
                # 入ってきたcellに正規化を充てる。
                cell = ntzreg.cellstr(cell)
                if label == "名前":
                    # ラベルが名前なら文字揃え処理をする。
                    cell = ntzstr.name5justify(cell)
                    tmp_df.append(cell)
                else:
                    # それ以外は仮dfへそのまま格納。
                    tmp_df.append(cell)
        df[label] = tmp_df


    ###################
    ##### 『つまむ』インデックスの生成
    # 『つまむ』元になるインデックス番号とスライス番号の配列
    anchor_index = ntzarr.pickcell(df["番号"])
    # 出力用のDateFrameを生成させておく。
    df_out = pd.DataFrame(columns = ["順番", "演奏曲", "演奏者", "使用楽器"])
    # 処理開始
    for label, out_label in zip(df.columns, df_out.columns):
        # 仮のコラム生成
        tmp_col = []
        # 番号以外を処理する。
        for start, pause in anchor_index:
            line = []
            for content in df[label][start: pause]:
                if isinstance(content, float):
                    continue
                else:
                    line.append(content)
            tmp_col.append("▽".join(line))
        df_out[out_label] = tmp_col
    
    # 番号だけ別処理する。
    tmp_arr = [int(num) for num in df["番号"].dropna(how="any")]
    df_out["順番"] = tmp_arr


    #####################
    # CSVとして書き出し
    to_gen_file = os.path.join('./_gen', filename)
    df_out.to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ["順番", "演奏曲", "演奏者", "使用楽器"],
        sep = ',')


    #####################
    ### オリジナルと中間ファイルを削除する。
    # 検証をするときはこれらを外す。
    os.remove(org_file)
    os.remove(to_tmp_file)