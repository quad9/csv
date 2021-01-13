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

# 月刊大阪弁護士会　会員異動　入会者用データを整理するためのコード

###################
##### 下準備

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
  columns=["カテゴリー", "登録番号", "氏名", "入会年月日", "退会年月日", "事務所", "郵便番号", "事務所住所１", "事務所住所２", "TEL", "FAX", "備考"],
  sep = ',')
df = pd.read_csv(path_to_tmp_file, encoding='utf-8')

# 全てNaNで埋められた行を取り除く処理をする。
df = df.dropna(how='all').dropna(how='all', axis = 1)


###################
##### 『つまむ』インデックス
# 『つまむ』元になるインデックス番号とスライス番号の配列
# 異動情報のカテゴリーごとに処理を分岐させるためのスライスを作成する。
# スライスを使って配列を作りたい場合。
anchor_index = ntzarr.pickcell(df["カテゴリー"])
# インデックス何番目から何番目までで値を指定したい場合。
anchor_index_i = ntzarr.pickcell(df["カテゴリー"], "i")
# スライス用　インデックス●番目から、最初から数えて●番目まで
other_index = [anchor_index[1][0], anchor_index[-1][-1]]


###################
##### dfの整理

##### df["登録番号"]
# フロートを文字列に変換する。
df["登録番号"] = df["登録番号"].astype('float').astype('int').astype('str')
df["登録番号"] = "【会員番号 " + df["登録番号"] + "】"


# 番号はintで上手く動かないので先にdf["登録番号"]をstrに変換してから処理。
# セル内の文字列を正規表現で整える。
for label in df.columns:
  tmp_df = []
  for cell in df[label]:
    if cell is np.nan:
      tmp_df.append(cell)
    else:
      tmp_df.append(ntzreg.cellstr(cell, "zs"))
  df[label] = tmp_df


##### df["会員名"]
df["会員名"] = [ntzstr.name5justify(name) for name in df["氏名"]]


##### df["会員名ルビ付"], df["入会年月日"], df["@写真名"]
for group in anchor_index:
  # 新入会員用のdf["会員名ルビ付"]、df["@写真名"]の生成と写真の連番串刺し処理。
  # 決め打ち。
  # 二次配列をforして、配列を一つずつ処理する。最初に抜き出された配列のインデック[0]番目は値が『0』とわかっているので。
  start = group[0]
  pause = group[1]
  tmp_out_dates = []

  if start == 0:
    ##### df["会員名ルビ付"]
    tmp_member_with_ruby = ntzstr.name5justify_with_ruby(df["氏名"][start: pause], df["備考"][start: pause])
    df["会員名ルビ付"] = tmp_member_with_ruby + [np.nan] * (other_index[1] - other_index[0])

    ##### df['入会年月日']
    tmp_join_dates = []
    # カテゴリーのグループをスライスを使って配列にし、それぞれに処理をしていく。
    for date in df["入会年月日"][start: pause]:
      year, month, day = [d.strip() for d in date.split("/")]
      wareky_date = f"{dt.wareky(int(year), int(month), int(day))}{month}月{day}日"
      tmp_join_dates.append(f"{wareky_date}付")
    df["入会年月日"] = tmp_join_dates + [np.nan] * (other_index[1] - other_index[0])

    ##### df["@写真名"]
    # 写真のファイル名をdfに格納する。
    tmp_photos = [os.path.basename(filename) for filename in sorted(glob.glob("./_org/*.psd"))]
    # 中間df["写真"]を生成する。写真枚数はコラム数より少ないので、不足分をNaNで埋める。
    df["写真"] = tmp_photos + [np.nan] * (other_index[1] - other_index[0])
    # df["@写真名"]に変換するための仮配列の生成。
    tmp_photo_labels = []
    # df["@写真名"]の生成と写真の異動およびリネーム。
    # 処理をしたグループの分（インデックス番号[0]番）を限定で処理する。
    for member, photo_label in zip(df["会員名"][start: pause], df["写真"][start: pause]):
      # 準備1
      # 『_org』ディレクトリにあるpsdファイル名をベース名と拡張子に取り分ける。
      # if photo_label is np.nan:
      #   continue
      # else:
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

    # 写真ファイルの移動とリネーム処理が終わってから最後にdfへ値を代入する。
    # df["@写真名"]の生成。
    df["@写真名"] = tmp_photo_labels + [np.nan] * (other_index[1] - other_index[0])


##### df["その他の会員名"]
tmp_others = []
for name in df["会員名"][other_index[0]: other_index[1]]:
  tmp_others.append(f"{name}氏")
df["その他の会員名"] = [np.nan] * (anchor_index[0][1] - anchor_index[0][0]) + tmp_others


##### df["退会年月日"]
tmp_out_dates = []
for index, date in enumerate(df["退会年月日"]):
  if date is np.nan:
    tmp_out_dates.append(np.nan)
  else:
    year, month, day = [d.strip() for d in date.split("/")]
    wareky_date = f"{dt.wareky(int(year), int(month), int(day))}{month}月{day}日"
    if anchor_index_i[1][0] <= index <= anchor_index_i[1][1]:
      tmp_out_dates.append(wareky_date)
    else:
      tmp_out_dates.append(f"{wareky_date}付")
df["退会年月日"] = tmp_out_dates


##### df["異動先弁護士会"]
tmp_asociations = []
for asociation in df["備考"][anchor_index[3][0]: anchor_index[3][1]]:
  tmp_asociations.append(f"{asociation}弁護士会")
df["異動先弁護士会"] = [np.nan] * (len(df) - len(tmp_asociations)) + tmp_asociations


###################
# CSVファイルに書き込んでいく。
# 範囲を示すインデックス作成
# 決め打ち。
# 新入会員はインデックス[0]番目。その他のカテゴリーは1番目以降最後までだから。
for group in anchor_index:
  # 新入会員用のdf["会員名ルビ付"]、df["@写真名"]の生成と写真の連番串刺し処理。
  # 決め打ち。
  # 二次配列をforして、配列を一つずつ処理する。最初に抜き出された配列のインデック[0]番目は値が『0』とわかっているので。
  start = group[0]
  pause = group[1]
  if start == 0:
    to_gen_file = os.path.join('./_gen', f"新入会員用_{filename}")
    # コラムを新入会員に限定してCSVの生成。
    df[anchor_index[0][0]: anchor_index[0][1]].to_csv(to_gen_file,
      encoding = "utf-16",
      index = False,
      columns = ["会員名ルビ付", "登録番号", "入会年月日", "事務所", "郵便番号", "事務所住所１", "事務所住所２", "TEL", "FAX", "@写真名"],
    sep = ',')
  else:
    to_gen_file = os.path.join('./_gen', f"その他_{filename}")
    df[other_index[0]: other_index[1]].to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ["その他の会員名", "登録番号", "退会年月日", "異動先弁護士会"],
        sep = '\t')


# #####################
# ### オリジナルと中間ファイルを削除する。
# # 検証をするときはこれらを外す。
os.remove(path_to_tmp_file)
shutil.rmtree("./_org")
os.mkdir("./_org")