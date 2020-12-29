import glob
import jaconv
import re
import pandas as pd
import sys
sys.path.append('../lib')
import t14i_regex

# 月刊大阪弁護士会　表3「今後の主な行事等」を整理するためのコード
# read CSV file
file_path = glob.glob("./*.csv")
file = file_path[0]
# create deta frame of pandas
df_in = pd.read_csv(file,
                    header = None,
                    names = ['日時', '時間', '内容', '場所'],
                    encoding = 'utf-8')

# lib/t14ireに渡してセル内の文字列を整理する。<<<<<<<<<<
df = t14i_regex.csv_reg(df_in)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 列の整理。
df['日時'] = '【日時】' + df['日時']
df['日付'] = df['日時'] + df['時間']
df['場所'] = '【場所】' + df['場所']
df['概要'] = df['日付'] + '▼' + df['場所']

# 変更した内容を元のファイルへ上書き保存する。
df.to_csv(file,
          encoding = "utf-8",
          index = False,
          columns = ['内容', '概要'],
          sep = '\t')
