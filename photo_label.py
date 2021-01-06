import os
import glob
import shutil
import re
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr
import ntzarr
import ntzdate as dt
# from lib import t14i_regex  #=> 同じ階層にlibディレクトリがある場合。

# 写真のファイル名を変更するコード

###################
# 下準備
# 読み込むCSVファイルは1枚だけが前提。
org_file = glob.glob("./_org/*.csv")[0]
filename = os.path.basename(org_file)
# create deta frame of pandas
df_in = pd.read_csv(org_file, encoding='utf-8')

# 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
path_to_tmp_file = os.path.join('./_tmp', filename)
df_in.to_csv(path_to_tmp_file,
  encoding = "utf-8",
  index = False,
  columns=["氏名"],
  sep = ',')
df = pd.read_csv(path_to_tmp_file, encoding='utf-8')

# セル内の文字列を正規表現で整える。
for label in df.columns:
  tmp_df = []
  for cell in df[label]:
    if cell is np.nan:
      tmp_df.append(cell)
    else:
      tmp_df.append(ntzreg.cellstr(cell))
  df[label] = tmp_df

tmp_members = []
for shimei in df["氏名"]:
  tmp_members.append(ntzstr.name5justify(shimei))

df["会員名"] = tmp_members

##### df["@写真名"]
# 写真のファイル名をdfに格納する。
photo_files_path = sorted(glob.glob("./_org/*.psd"))
df["写真"] = [os.path.basename(filename) for filename in photo_files_path]

# df["@写真名"]に変換するための仮配列の生成。
tmp_photo_labels = []
# df["@写真名"]の生成と写真の異動およびリネーム。
for member, photo_label in zip(df["会員名"], df["写真"]):
  # 準備1
  # 『_org』ディレクトリにあるpsdファイル名をベース名と拡張子に取り分ける。
  basename, ext = os.path.splitext(photo_label)
  # 変更後のファイル名を変数に格納する。
  renwal_label = f"img{basename}_{member}{ext}"
  # 準備2
  # 写真を『_gen』ディレクトリにコピーする。
  # 『copy2()』メソッドは、コピー元のファイルのメタデータを保存したい場合に使用する。
  shutil.copy2(f"./_org/{photo_label}", f"./_gen/{photo_label}")
  # 写真のファイル名を書き換える。
  # 書き換えたいのは、
  # 第一引数　『どの階層の何というファイル名』で、
  # 第二引数　『どの階層の何というファイル名』に書き換えるのか。
  # という書き方に注意をする。
  os.rename(f"_gen/{photo_label}", f"_gen/{renwal_label}")
  # df["@写真名"]に変換する仮配列へ格納する。
  tmp_photo_labels.append(renwal_label)
# df["@写真名"]の生成。
df["@写真名"] = tmp_photo_labels + [np.nan] * ( len(df) - len(tmp_photo_labels) )

###################
# CSVファイルに書き込んでいく。
# 新入会員用のCSVに書き出す。
to_gen_file = os.path.join('./_gen', f"写真ファイル名整理_{filename}")
df.to_csv(to_gen_file,
    encoding = "utf-8",
    index = False,
    columns = ["@写真名"],
    sep = ',')


#####################
### オリジナルと中間ファイルを削除する。
# 検証をするときはこれらを外す。
os.remove(org_file)
for file_path in photo_files_path:
  os.remove(file_path)
os.remove(path_to_tmp_file)