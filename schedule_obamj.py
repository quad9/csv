import glob
import jaconv
import re
import pandas as pd
import sys
sys.path.append('../lib')
import t14i_regex
# 同じ階層にlibディレクトリがある場合。
# from lib import t14i_regex

# 月刊大阪弁護士会　研修情報用データを整理するためのコード

# read CSV file
file_path = glob.glob("./*.csv")
file = file_path[0]
# create deta frame of pandas
df_in = pd.read_csv(file, encoding = 'utf-8')
# lib/t14ireに渡してセル内の文字列を整理する。<<<<<<<<<<
df = t14i_regex.csv_reg(df_in)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# print(df['区分'])
# 列の整理。
df['区分'] = '【' + df['区分'] + '】'
df['専門'] = '【' + df['専門'] + '】'
df['分野別'] = '【分野別登録弁護士制度指定研修（' + df['分野別'] + '）】'
tmp_date = []
for cell in df['実施日']:
    cell = re.sub('(\d\d?)月(\d\d?)日（([月火水木金土日])）', r'\1/\2\3', cell)
    tmp_date.append(cell)
df['実施日'] = tmp_date
# 列の入替
df['日時'] = df['区分'] + df['専門'] + '▼' + df['実施日'] + '▼' + df['実施時間']
df['単位'] = df['継続\n研修\n単位数']
tmp_teacher = []
for cell in df['講師']:
    cell = re.sub('▽', '、', cell)
    tmp_teacher.append(cell)
df['講師'] = tmp_teacher
df['内容'] = df['分野別'] + '▼' + df['研修等の名称'] + '▼◇' + df['講師']
df['備考'] = '◆' + df['主催者'] + '▼□' + df['参加資格等'] + '／' + df['参加費'] + '▼■' + df['実施場所'] + '▼' + df['一時保育']
# 変更した内容を元のファイルへ上書き保存する。
df.to_csv(file,
    encoding = "utf-8",
    index = False,
    columns = ['日時', '単位', '内容', '備考'],
    sep = '\t')
