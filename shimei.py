import glob
import os
import pandas as pd
import sys
sys.path.append('../lib')
import t14i_regex
import t14i_datetime as dt

# from lib import t14i_regex  #=> 同じ階層にlibディレクトリがある場合。

# 大東楽器　氏名の整理

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
    if uji_size == 1 and mei_size ==1:
      tmp_name.append(f'{arr[0]}{arr[1]}')
    elif uji_size == 2 and mei_size == 2:
      tmp_name.append(f'{arr[0][0]}　{arr[0][1]}　{arr[1][0]}　{arr[1][1]}')
    elif uji_size == 1 and mei_size == 2:
      tmp_name.append(f'{arr[0]}　　　{arr[1][0]}　{arr[1][1]}')
    elif uji_size == 2 and mei_size == 1:
      tmp_name.append(f'{arr[0][0]}　{arr[0][1]}　　　{arr[1]}')
    elif uji_size == 1 and mei_size == 3 or uji_size == 3 and mei_size == 1:
      tmp_name.append(f'{arr[0]}　　　{arr[1]}')
    elif uji_size == 2 and mei_size == 3:
      tmp_name.append(f'{arr[0][0]}　{arr[0][1]}　{arr[1]}')
    elif uji_size == 3 and mei_size == 2:
      tmp_name.append(f'{arr[0]}　{arr[1][0]}　{arr[1][1]}')
    else:
      tmp_name.append('')

# # 全ての変更を上書き保存
# df.to_csv(csv_file,
#     encoding = "utf-16",
#     index = False,
#     columns = ('氏名ルビ付','②所属部等','③修習期','④前任地','⑤前々任地','一言又は趣味など','@写真名'),
#     sep = ',')
