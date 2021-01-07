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
  columns=["カテゴリー", "氏名", "入会年月日", "備考"],
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


###################
# dfの整理

##### 『つまむ』インデックス
# 『つまむ』元になるインデックス番号とスライス番号の配列
# 異動情報のカテゴリーごとに処理を分岐させるためのスライスを作成する。
# スライスを使って配列を作りたい場合。
anchor_index = ntzarr.pickcell(df["カテゴリー"])
# インデックス何番目から何番目までで値を指定したい場合。
anchor_index_i = ntzarr.pickcell(df["カテゴリー"], "i")

##### df['入会年月日']
tmp_dates = []
# カテゴリーのグループをスライスを使って配列にし、それぞれに処理をしていく。
for group in anchor_index:
  for date in df["入会年月日"][group[0]: group[1]]:
    year, month, day = [d.strip() for d in date.split("/")]
    wareky_date = f"{dt.wareky(int(year), int(month), int(day))}{month}月{day}日"
    if "訃報" in df["カテゴリー"][group[0]]:
      tmp_dates.append(wareky_date)
    else:
      tmp_dates.append(f"{wareky_date}付")
df["入会年月日"] = tmp_dates

##### df["会員名"]
df["会員名"] = [ntzstr.name5justify(name) for name in df["氏名"]]


###################
# CSVファイルに書き込んでいく。
# 範囲を示すインデックス作成
# 決め打ち。
# 新入会員はインデックス[0]番目。その他のカテゴリーは1番目以降最後までだから。
other_index = [anchor_index[1][0], anchor_index[-1][-1]]

for group in anchor_index:
  # 新入会員用のdf["会員名ルビ付"]、df["@写真名"]の生成と写真の連番串刺し処理。
  # 決め打ち。
  # 二次配列をforして、配列を一つずつ処理する。最初に抜き出された配列のインデック[0]番目は値が『0』とわかっているので。
  if group[0] == 0:
    ##### df["会員名ルビ付"]
    df["会員名ルビ付"] = ntzstr.name5justify_with_ruby(df["氏名"], df["備考"])

    ##### df["@写真名"]
    # 写真のファイル名をdfに格納する。
    tmp_photos = [os.path.basename(filename) for filename in sorted(glob.glob("./_org/*.psd"))]
    # 中間df["写真"]を生成する。写真枚数はコラム数より少ないので、不足分をNaNで埋める。
    df["写真"] = tmp_photos + [np.nan] * ( len(df) - len(tmp_photos) )
    # df["@写真名"]に変換するための仮配列の生成。
    tmp_photo_labels = []
    # df["@写真名"]の生成と写真の異動およびリネーム。
    # 処理をしたグループの分（インデックス番号[0]番）を限定で処理する。
    for member, photo_label in zip(df["会員名"][0: group[1]], df["写真"][0: group[1]]):
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
    # 写真ファイルの移動とリネーム処理が終わってから最後にdfへ値を代入する。
    # df["@写真名"]の生成。
    df["@写真名"] = tmp_photo_labels + [np.nan] * ( len(df) - len(tmp_photo_labels) )

    # 新入会員用のCSVに書き出す。
    to_gen_file = os.path.join('./_gen', f"新入会員用_{filename}")
    # コラムを新入会員に限定してCSVの生成。
    df[group[0]: group[1]].to_csv(to_gen_file,
        encoding = "utf-16",
        index = False,
        columns = ["カテゴリー", "会員名ルビ付", "@写真名", "入会年月日"],
        sep = ',')
  else:
    to_gen_file = os.path.join('./_gen', f"その他_{filename}")
    df[other_index[0]: other_index[1]].to_csv(to_gen_file,
        encoding = "utf-8",
        index = False,
        columns = ["カテゴリー", "会員名", "入会年月日"],
        sep = '\t')
columns = ('会員名','入会年月日'),    
# columns = ('会員名ルビ付','登録番号','入会年月日','事務所','郵便番号','事務所住所１','事務所住所２','TEL','FAX','@写真名'),    




# #####################
# ### オリジナルと中間ファイルを削除する。
# # 検証をするときはこれらを外す。
# os.remove(org_file)
# os.remove(to_tmp_file)