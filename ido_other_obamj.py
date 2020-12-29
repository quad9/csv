import glob
import pandas as pd
import sys
sys.path.append('../lib')
import t14i_regex
import t14i_string as st
import t14i_datetime as dt

# 同じ階層にlibディレクトリがある場合。
# from lib import t14i_regex

# 月刊大阪弁護士会　会員異動　退会、登録替、訃報用データを整理するためのコード

# read CSV file
csv_file_path = glob.glob("./*.csv")
csv_file = csv_file_path[0]
# create deta frame of pandas
df_in = pd.read_csv(csv_file, encoding = 'utf-8')
# lib/t14ireに渡してセル内の文字列を整理する。<<<<<<<<<<
df = t14i_regex.csv_reg(df_in)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 氏名を5文字で揃える。
df['氏名'] = st.namaezoroe(df['氏名'])
df['氏名'] = df['氏名'] + '氏'

# 登録番号を括弧で囲む。
df['登録番号'] = '【会員番号 ' + df['登録番号'] + '】'
# print(df['登録番号'])
# 日付のフォーマットを変更する。
tmp_date = []
for d in df['退会年月日']:
    y, m, d = d.split('/')
    y = dt.wareky(int(y), int(m), int(d))
    tmp_date.append(f'{y}{m}月{d}日付')
df['退会年月日'] = tmp_date

# # 他会への移籍
# # ifで空白を回避させてプログラムを進めたいが、インデックスが合わないと怒られる。
# tmp_aso = []
# for s in df['備考']:
#     if s == 'nan':
#         next
#     else:
#         tmp_aso.append(f'{s}弁護士会')
df['備考'] += '弁護士会'
# 上のif文が上手くいかないから、こちらで不要なセルを削除して対応する。
tmp_words = []
for cell in df['備考']:
    cell = cell.replace('nan弁護士会', '')
    tmp_words.append(cell)
df['備考'] = tmp_words

# 全ての変更を上書き保存
df.to_csv(csv_file,
          encoding = "utf-16",
          index = False,
          columns = ('氏名', '登録番号', '退会年月日', '備考'),
          sep = '\t')
