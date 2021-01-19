import glob
import jaconv
import re
import pandas as pd
import csv
from qreki import Kyureki
import sys
sys.path.append('../lib')
import t14i_regex

# カレンダーに六曜を付与するプログラム

# read CSV file
files = glob.glob("./*.csv")
df = pd.read_csv(files[0], encoding='utf-8')

tmp_month = []
tmp_day = []
tmp_rokuyou =[]

for str in df['日付']:
  arr = str.split('/')
  tmp_month.append(arr[1])
  tmp_day.append(arr[2])
  
  ymd = Kyureki.from_ymd(int(arr[0]), int(arr[1]), int(arr[2]))
  tmp_rokuyou.append(ymd.rokuyou)


df['月'] = tmp_month
df['日'] = tmp_day
df['六曜'] = tmp_rokuyou

# 全ての変更を上書き保存
df.to_csv("カレンダー.csv",
  encoding="utf-16",
  index=False,
  columns=('月', '日', '六曜', '祝日'),
  sep=',')
