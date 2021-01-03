import os
import glob
import re
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import ntzreg
import ntzstr
import ntzarr
import ntzdate
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
    columns=["カテゴリー", "氏名"],
    sep = ',')
df = pd.read_csv(path_to_tmp_file, encoding='utf-8')

# 処理をカテゴリーごとに分岐させる前に『写真ファイル名用の氏名』の整理。
df["写真用氏名"] = [ntzstr.name5justify(name) for name in df["氏名"]]
df["写真"] = [os.path.basename(filename) for filename in sorted(glob.glob("./_org/*.psd"))]

tmp_photo_name = []
for name, photo in zip(df["写真用氏名"], df["写真"]):
  basename, ext = os.path.splitext(photo)
  tmp_photo_name.append(f"img{basename}_{name}{ext}")
df["@写真名"] = tmp_photo_name
print(df["@写真名"])

# # 設定した写真名をファイルに一括でファイル名を上書きする。
# i = 0
# for file_name in photo_file_path:
#   os.rename(file_name, df['@写真名'][i])
#   i += 1
# # 処理をカテゴリーごとに分岐させる前に『写真』の整理。

# # 処理をカテゴリーごとに分岐させる前に『df['入会年月日']』の整理。
# # df['入会年月日']
# tmp_date = []
# for date in df['入会年月日']:
#   y, m, d = [date.strip() for date in str.split("/")]
#   y = dt.wareky(int(y), int(m), int(d))
#   tmp_date.append(f'{y}{m}月{d}日付')
# df['入会年月日'] = tmp_date


# 処理をカテゴリーごとに分岐させる前に『』の整理。
# 処理をカテゴリーごとに分岐させる前に『』の整理。
# 処理をカテゴリーごとに分岐させる前に『』の整理。
# 処理をカテゴリーごとに分岐させる前に『』の整理。
# 処理をカテゴリーごとに分岐させる前に『』の整理。

# # 異動情報のカテゴリーごとに処理を分岐させる。
# # 処理をつまむためのスライスを作成する。
# anchor_index = ntzarr.pickcell(df["カテゴリー"])
# # カテゴリーごとに分岐させて処理をする。
# for scope in anchor_index:
#   if scope[scope[0]: scope[1]]:
#     print("会員異動の処理はここへ書く。")
#   else:
#     if "訃報" in df["カテゴリー"][scope[0]]:
#       print("訃報の連絡はこちらへ。")
#     else:
#       print("それ以外の処理はこちらへ書く。")



###################
# CSVに上書きで書き出し完成
to_gen_file = os.path.join('./_gen', filename)
df.to_csv(to_gen_file,
    encoding = "utf-8",
    index = False,
    columns=["カテゴリー", "氏名"],
    sep = '\t')


# #####################
# ### オリジナルと中間ファイルを削除する。
# # 検証をするときはこれらを外す。
# os.remove(org_file)
# os.remove(to_tmp_file)



# # read CSV file
# csv_file_path = glob.glob("./*.csv")
# csv_file = csv_file_path[0]
# # create deta frame of pandas
# df_in = pd.read_csv(csv_file, encoding = 'utf-8')
# # lib/t14ireに渡してセル内の文字列を整理する。<<<<<<<<<<
# df = t14i_regex.csv_reg(df_in)
# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# # 氏名を5文字で揃える。写真ファイルに付ける氏名用。
# tmp_name = []
# for str in df['氏名']:
#     arr = str.split()
#     uji = arr[0]
#     mei = arr[1]
#     uji_size = len(arr[0])
#     mei_size = len(arr[1])
#     if uji_size == 2 and mei_size == 2:
#         tmp_name.append(f'{arr[0]}　{arr[1]}')
#     elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
#         tmp_name.append(f'{arr[0]}　　{arr[1]}')
#     elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
#         tmp_name.append(f'{arr[0]}　{arr[1]}')
#     elif uji_size == 2 and mei_size == 3 or uji_size == 3 and mei_size == 2:
#         tmp_name.append(f'{arr[0]}{arr[1]}')
#     else:
#         tmp_name.append('')
# df['氏名写真用'] = tmp_name

# # 氏名にルビを付ける。
# tmp_df = (df['氏名'] + ' ' + df['備考'])
# tmp_name_ruby = []
# for str in tmp_df:
#     arr = str.split()
#     uji_size = len(arr[0])
#     mei_size = len(arr[1])
#     if uji_size == 2 and mei_size == 2:
#         tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}]　[{arr[1]}/{arr[3]}]')
#     elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
#         tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}]　　[{arr[1]}/{arr[3]}]')
#     elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
#         tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}]　[{arr[1]}/{arr[3]}]')
#     elif uji_size == 2 and mei_size == 3 or uji_size == 3 and mei_size == 2:
#         tmp_name_ruby.append(f'[{arr[0]}/{arr[-2]}][{arr[1]}/{arr[-1]}]')
#     else:
#         tmp_name_ruby.append('')
# df['氏名ルビ付'] = tmp_name_ruby


# # 全ての変更を上書き保存
# df.to_csv(csv_file,
#           encoding = "utf-16",
#           index = False,
#           columns = ('氏名ルビ付','登録番号','入会年月日','事務所','郵便番号','事務所住所１','事務所住所２','TEL','FAX','@写真名'),
#           sep = ',')
