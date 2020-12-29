import glob
import jaconv
import re
import pandas as pd
import csv
import sys
sys.path.append('../lib')
import t14i_regex

# CSVファイルの構造は変えず、字句のみ正規表現で整理するコード。
log = '''
元のファイルのヘッダーを活かしますか？
-----------------------------------------
ヘッダーを活かす => 0　ヘッダーを取り去る => 1
どちらかの数値を入力してください。

>> '''
ans = int(input(log))
if ans == 0:
    responce = True
else:
    responce = False

file_path = glob.glob("./*.csv")
for file in file_path:
    df_in = pd.read_csv(file, encoding = 'utf-8')
    df = t14i_regex.csv_reg(df_in)
    df.to_csv(file,
                  encoding = "utf-8",
                  header = responce,
                  index = False,
                  sep = '\t')
