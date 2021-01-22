import os
import pandas as pd
import numpy as np
import csv
import calendar
import pprint

# # 任意の月のカレンダー出力
# print(calendar.month(2021, 1))

# =>
#     January 2021
# Mo Tu We Th Fr Sa Su
#              1  2  3
#  4  5  6  7  8  9 10
# 11 12 13 14 15 16 17
# 18 19 20 21 22 23 24
# 25 26 27 28 29 30 31


# # このインスタンスはString型
# print(type(calendar.month(2021, 1)))

# => <class 'str'>


# # 年間カレンダーの出力
# print(calendar.calendar(2021))

# =>
#                                   2021

#       January                   February                   March
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#              1  2  3       1  2  3  4  5  6  7       1  2  3  4  5  6  7
#  4  5  6  7  8  9 10       8  9 10 11 12 13 14       8  9 10 11 12 13 14
# 11 12 13 14 15 16 17      15 16 17 18 19 20 21      15 16 17 18 19 20 21
# 18 19 20 21 22 23 24      22 23 24 25 26 27 28      22 23 24 25 26 27 28
# 25 26 27 28 29 30 31                                29 30 31

#        April                      May                       June
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#           1  2  3  4                      1  2          1  2  3  4  5  6
#  5  6  7  8  9 10 11       3  4  5  6  7  8  9       7  8  9 10 11 12 13
# 12 13 14 15 16 17 18      10 11 12 13 14 15 16      14 15 16 17 18 19 20
# 19 20 21 22 23 24 25      17 18 19 20 21 22 23      21 22 23 24 25 26 27
# 26 27 28 29 30            24 25 26 27 28 29 30      28 29 30
#                           31

#         July                     August                  September
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#           1  2  3  4                         1             1  2  3  4  5
#  5  6  7  8  9 10 11       2  3  4  5  6  7  8       6  7  8  9 10 11 12
# 12 13 14 15 16 17 18       9 10 11 12 13 14 15      13 14 15 16 17 18 19
# 19 20 21 22 23 24 25      16 17 18 19 20 21 22      20 21 22 23 24 25 26
# 26 27 28 29 30 31         23 24 25 26 27 28 29      27 28 29 30
#                           30 31

#       October                   November                  December
# Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
#              1  2  3       1  2  3  4  5  6  7             1  2  3  4  5
#  4  5  6  7  8  9 10       8  9 10 11 12 13 14       6  7  8  9 10 11 12
# 11 12 13 14 15 16 17      15 16 17 18 19 20 21      13 14 15 16 17 18 19
# 18 19 20 21 22 23 24      22 23 24 25 26 27 28      20 21 22 23 24 25 26
# 25 26 27 28 29 30 31      29 30                     27 28 29 30 31


# # 週の始まりの曜日を指定する。メソッドを充てて指定しないとデフォルトは月曜日。
#   "calendar.MONDAY"で帰ってくるのは　=> 0
#   "calendar.SUNDAY"で帰ってくるのは　=> 6
#   整数を引数として入れてやってもよい。
# calendar.setfirstweekday(calendar.SUNDAY)
# # このインスタンスはイミュータブル。そのまま出力する。
# print(calendar.month(2021, 1))


# # 日本語にローカライズドさせる。
# ltc_ja = calendar.LocaleTextCalendar(locale='ja_jp')
# print(ltc_ja.formatmonth(2021, 1))


# # 一月分のカレンダーを配列として出力する。
# calendar.setfirstweekday(calendar.SUNDAY)
# calendar.monthcalendar(2021, 1)


###################
# # 下準備
# # ファイルは1枚だけが前提。
# org_file = glob.glob("./_org/*.csv")[0]
# filename = os.path.basename(org_file)
# # create deta frame of pandas
# df_in = pd.read_csv(org_file, encoding='utf-8')

# # 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
# path_to_tmp_file = os.path.join('./_tmp', filename)
# df_in.to_csv(path_to_tmp_file,
#     encoding = "utf-8",
#     index = False,
#     columns=["日時", "時間", "内容", "場所", "備考"],
#     sep = ',') 
# df = pd.read_csv(path_to_tmp_file, encoding = "utf-8")


# calendar.monthcalendar(2021, 1)
# calendar.monthcalendar(2021, 1)

# df = pd.DataFrame(calendar.yeardayscalendar(2021),
#                   columns = ["日", "月", "火", "水", "木", "金", "土"])

def createcal(year):
  year_dfs = []
  calendar.setfirstweekday(calendar.SUNDAY)
  for month in range(1,13):
    print(pd.DataFrame(calendar.monthcalendar(year, month),
                      columns = ["日", "月", "火", "水", "木", "金", "土"]))
  # return year_dfs

createcal(2021)
    






# print(df)
# cal = calendar.Calendar(firstweekday=6)
# pprint.pprint(cal.yeardayscalendar(2021))
# pprint.pprint(cal.yeardays2calendar(2021))


# df = pd.DataFrame(cal.yeardayscalendar(2021),
#                   columns = ["日", "月", "火", "水", "木", "金", "土"])
# print(df)

# # CSVとして書き出し
# filename = "calender.csv"
# to_gen_file = os.path.join('./_gen', filename)
# df.to_csv(to_gen_file,
#     encoding = "utf-8",
#     index = False,
#     # columns = ["日", "月", "火", "水", "木", "金", "土"],
#     sep = ',')


# #とあるシステムのカレンダーマスタを用意する。

# import csv
# import datetime
# import locale
# import jpholiday


# #指定した日付の範囲を返す関数、ループ処理用
# def date_range(start_date: datetime, end_date: datetime):
#     diff = (end_date - start_date).days + 1
#     return (start_date + datetime.timedelta(i) for i in range(diff))

# return date_range(start_date: 2021, 1, 1, end_date: 2021, 12, 31)

# #指定した日付の曜日(日本語名)を返却
# #以下が文字化けするので、仕方なく、get_youbi関数を作った。。。
# #locale.setlocale(locale.LC_TIME, 'ja_JP.utf-8')
# #print(locale.getlocale(locale.LC_TIME))
# #youbi = atday.strftime('%A')
# def get_youbi(st_date:datetime)-> str:
#     # 曜日情報の文字列表現
#     week_name_list='月火水木金土日'
#     youbi = '%s曜日' % week_name_list[st_date.weekday()]
#     return youbi


# #指定したCSVのヘッダーを読み込み関数
# def getcsvheader(fname:str)->list:
#     #辞書として読み込み
#     with open(fname, encoding="cp932") as f:
#         reader = csv.DictReader(f)
#         ks = reader.fieldnames
#         return ks

# #カレンダーCSV生成処理
# #fname:ファイル名
# #smode:1,銀行カレンダーモード , 2:会社営業日カレンダーモード
# #sdate:生成開始日付
# #edate:生成終了日付
# # 土日祝のみのレコードを生成する。
# def create_calender_csv(fname:str,smode:int,sdate:datetime,edate:datetime):

#     with open(fname, "w", newline="") as f:
#         # 要素順を指定します（dictでは順序がわからないため）
#         hdlist = getcsvheader(".\\CAL\\_カレンダーマスタヘッダ.csv")

#         # writerオブジェクトを作成します.
#         writer = csv.DictWriter(f, fieldnames=hdlist, delimiter=",", quotechar='"')

#         # writeheaderでヘッダーを出力できます.
#         writer.writeheader()

#         range_date = date_range(sdate,edate)
#         for atday in range_date:
#             #出力する対象か判定する
#             outflag = False

#             #祝日判定
#             holiday_name = jpholiday.is_holiday_name(atday)
#             if holiday_name is not None:
#                 outflag = True

#             #土日判定
#             if atday.weekday() >= 5:
#                 outflag = True

#             if outflag == False:
#                 #出力せず次の日付へ
#                 continue

#             #曜日(日本語名)を取得
#             youbi = get_youbi(atday)

#             #休日名称の設定
#             if holiday_name is None:
#                 if smode == 1:
#                     #銀行モードは、祝日じゃなければ曜日を設定
#                     holiday_name = youbi
#                 elif smode == 2:
#                     #会社モードは、祝日じゃなければ、各社で名付ける休日名を設定
#                     if atday.weekday() == 5:
#                         holiday_name = "土曜休日"
#                     elif atday.weekday() == 6:
#                         holiday_name = "普通休日"

#             #モードによって、カレンダーコードの指定
#             if smode == 1:
#                 cal_code = "01"
#             elif smode == 2:
#                 cal_code = "0000000001"

#             writer.writerow(
#                     { 
#                         "カレンダコード"  : cal_code,
#                         "日付"  : atday.strftime('%Y%m%d') ,
#                         "日付名"  : holiday_name,
#                         "曜日"  : youbi,
#                         "削除フラグ"  : "0",
#                     }
#             )


# def main():

#     #生成するカレンダーの範囲
#     sdate = datetime.date(2020, 4, 1)
#     edate = datetime.date(2021, 3, 31)
#     #関数呼び出しとメイン処理
#     create_calender_csv("銀行用.csv",1,sdate,edate)
#     create_calender_csv("会社カレンダー用.csv",2,sdate,edate)



# if __name__ == '__main__': main()





# import glob
# import shutil
# import jaconv
# import re
# import pprint
# import pandas as pd
# import numpy as np
# import sys
# sys.path.append('../lib')
# import ntzreg
# import ntzstr
# # from lib import ntzreg  #=> 同じ階層にlibディレクトリがある場合。

# import csv
# from qreki import Kyureki
# import t14i_regex



# # カレンダーに六曜を付与するプログラム
# # 何曜日か始まるかによって先頭にNaNを入れていくように改良する。

# # read CSV file
# files = glob.glob("./*.csv")
# df = pd.read_csv(files[0], encoding='utf-8')

# tmp_month = []
# tmp_day = []
# tmp_rokuyou =[]

# for str in df['日付']:
#   arr = str.split('/')
#   tmp_month.append(arr[1])
#   tmp_day.append(arr[2])
  
#   ymd = Kyureki.from_ymd(int(arr[0]), int(arr[1]), int(arr[2]))
#   tmp_rokuyou.append(ymd.rokuyou)


# df['月'] = tmp_month
# df['日'] = tmp_day
# df['六曜'] = tmp_rokuyou

# # 全ての変更を上書き保存
# df.to_csv("カレンダー.csv",
#   encoding="utf-16",
#   index=False,
#   columns=('月', '日', '六曜', '祝日'),
#   sep=',')




# #########################################################################
# # df_in => df => df_outという流れにしたい場合。
# # fillnaしたかっtり、空行、空列を削除するなど出力前に整理整頓をしたい場合に有効と
# # 考えて今はこの流れにしている。
# # サンプルとして、daito_valentine_concert.pyの後半を参照のこと。
# # 将来書く力が付いたら、この流れは再検討する。

# # 出力ファイル用にコラムを収集して書き出す。
# df_out = df.reindex(columns = ["日時", "時間", "内容", "場所"])
# # df_out = df.reindex(columns = ["内容", "概要"])

# # セルをつまむ処理をしたので全てNaNで埋められた行が発生する。
# # これらを取り除く処理をする。
# df_out = df_out.dropna(how='all').dropna(how='all', axis = 1)
# #########################################################################

# # CSVとして書き出し
# to_gen_file = os.path.join('./_gen', filename)
# df_out.to_csv(to_gen_file,
#     encoding = "utf-8",
#     index = False,
#     columns = ["日時", "時間", "内容", "場所"],
#     sep = ',')


# # 行を順に表示させる。
# # つまり行ごとの配列を操作するきっかけを作る。
# # for i in range(len(df)):
# #     print(df.loc[i])
# # print(df.loc[0])