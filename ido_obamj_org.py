import glob
import os
import pandas as pd
import sys
sys.path.append('../lib')
import t14i_regex
import t14i_datetime as dt

# from lib import t14i_regex  #=> 同じ階層にlibディレクトリがある場合。

# 月刊大阪弁護士会　会員異動　入会者用データを整理するためのコード

# read CSV file
csv_file_path = glob.glob("./*.csv")
csv_file = csv_file_path[0]
# create deta frame of pandas
df_in = pd.read_csv(csv_file, encoding = 'utf-8')
# lib/t14ireに渡してセル内の文字列を整理する。<<<<<<<<<<
df = t14i_regex.csv_reg(df_in)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 氏名を5文字で揃える。写真ファイルに付ける氏名用。
tmp_name = []
for str in df['氏名']:
    arr = str.split()
    uji = arr[0]
    mei = arr[1]
    uji_size = len(arr[0])
    mei_size = len(arr[1])
    if uji_size == 2 and mei_size == 2:
        tmp_name.append(f'{arr[0]}　{arr[1]}')
    elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
        tmp_name.append(f'{arr[0]}　　{arr[1]}')
    elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
        tmp_name.append(f'{arr[0]}　{arr[1]}')
    elif uji_size == 2 and mei_size == 3 or uji_size == 3 and mei_size == 2:
        tmp_name.append(f'{arr[0]}{arr[1]}')
    else:
        tmp_name.append('')
df['氏名写真用'] = tmp_name

# 氏名にルビを付ける。
tmp_df = (df['氏名'] + ' ' + df['備考'])
tmp_name_ruby = []
for str in tmp_df:
    arr = str.split()
    uji_size = len(arr[0])
    mei_size = len(arr[1])
    if uji_size == 2 and mei_size == 2:
        tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}]　[{arr[1]}/{arr[3]}]')
    elif uji_size == 1 and mei_size == 2 or uji_size == 2 and mei_size == 1:
        tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}]　　[{arr[1]}/{arr[3]}]')
    elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
        tmp_name_ruby.append(f'[{arr[0]}/{arr[2]}]　[{arr[1]}/{arr[3]}]')
    elif uji_size == 2 and mei_size == 3 or uji_size == 3 and mei_size == 2:
        tmp_name_ruby.append(f'[{arr[0]}/{arr[-2]}][{arr[1]}/{arr[-1]}]')
    else:
        tmp_name_ruby.append('')
df['氏名ルビ付'] = tmp_name_ruby

# 日付のフォーマットを変更する。
tmp_date = []
for d in df['入会年月日']:
    y, m, d = d.split('/')
    y = dt.wareky(int(y), int(m), int(d))
    tmp_date.append(f'{y}{m}月{d}日付')
df['入会年月日'] = tmp_date

# read psd file
photo_file_path = sorted(glob.glob("./*.psd"))
tmp_photo = []
for photo_file in photo_file_path:
    basename, ext = os.path.splitext( os.path.basename(photo_file))
    tmp_photo.append(basename)
df['元ファイル名'] = sorted(tmp_photo)
df['@写真名'] = 'img' + df['元ファイル名'] + '_' + df['氏名写真用'] + '.psd'

# 設定した写真名をファイルに一括でファイル名を上書きする。
i = 0
for file_name in photo_file_path:
  os.rename(file_name, df['@写真名'][i])
  i += 1

# 全ての変更を上書き保存
df.to_csv(csv_file,
          encoding = "utf-16",
          index = False,
          columns = ('氏名ルビ付','登録番号','入会年月日','事務所','郵便番号','事務所住所１','事務所住所２','TEL','FAX','@写真名'),
          sep = ',')
