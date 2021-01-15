import os
import glob
import shutil
import re
import pprint
import pandas as pd
import numpy as np
import sys
sys.path.append("../lib")
import ntzreg
import ntzstr
import ntzarr
import ntzdate as dt
# 同じ階層にlibディレクトリがある場合。
# from lib import t14i_regex

# 月刊大阪弁護士会　研修情報用データを整理するためのコード

########## 入力
# 読み込むCSVファイルは1枚だけが前提。
org_file = glob.glob("./_org/*.csv")[0]
filename = os.path.basename(org_file)
# create deta frame of pandas
df_in = pd.read_csv(org_file, encoding = "utf-8")


########## 中間ファイル作成
# 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
path_to_tmp_file = os.path.join("./_tmp", filename)
df_in.to_csv(path_to_tmp_file,
    encoding = "utf-8",
    index = False,
    columns=["実施日", "実施時間", "単位数", "実施形態", "区分", "専門", "分野別", "研修等の名称", "講師", "主催者", "実施場所", "参加費", "参加資格等", "一時保育", "完全事前申込制"],
    sep = ",")
df = pd.read_csv(path_to_tmp_file, encoding="utf-8")


########## dfの空欄を『〓』で埋めておく。
for label in df:
    if re.search(r"専門|分野別|完全事前申込制", label):
        continue
    else:
        df[label] = df[label].fillna("〓〓〓〓〓〓〓")


########## セル内の文字列を正規表現で整形
# セル内が空欄の時に起こるエラー　int, floatが『elif cell is np.nan:』の
# 条件分岐で上手く作用してくれないので、『if isinstance(cell, 性質):』で解決している。
for label in df.columns:
    tmp_df = []
    for cell in df[label]:
        if isinstance(cell, float):
            tmp_df.append(cell)
        elif isinstance(cell, int):
            tmp_df.append(cell)
        elif cell is np.nan:
            tmp_df.append(cell)
        else:
            tmp_df.append(ntzreg.cellstr(cell, "zs"))
    df[label] = tmp_df


########## 列の整理

########## df["区分・専門"]の生成
##### df["区分"], df["専門"]の整理
# 『np.nan』が無効になる場合、『isinstance』が有効！！！！！！
# というより、『isinstance』一択ではないか？？？？
df["区分"] = "【" + df["区分"] + "】"
tmp_div = []
for div, sp in zip(df["区分"], df["専門"]):
    if isinstance(sp, float):
        tmp_div.append(div)
    else:
        tmp_div.append(f"{div}{sp}")
df["区分・専門"] = tmp_div


########## df["研修内容"]の生成
##### df["分野別"]の整理
tmp_field = []
for field in df["分野別"]:
    if isinstance(field, float):
        tmp_field.append(field)
    else:
        tmp_field.append(f'分野別登録弁護士制度指定研修（{field}）')
df["分野別"] = tmp_field


# df["講師"] = df["講師"].fillna("〓〓〓〓〓〓〓")
# print(df["講師"][0])
# # df["内容"] = df["分野別"] + "▼" + df["研修等の名称"] + "▼◇" + df["講師"]
# # print(df["区分・専門"])

# # df[""]


# tmp_date = []
# for cell in df["実施日"]:
#     cell = re.sub("(\d\d?)月(\d\d?)日（([月火水木金土日])）", r"\1/\2\3", cell)
#     tmp_date.append(cell)
# df["実施日"] = tmp_date
# # 列の入替
# df["日時"] = df["区分"] + df["専門"] + "▼" + df["実施日"] + "▼" + df["実施時間"]
# df["単位"] = df["継続\n研修\n単位数"]
# tmp_teacher = []
# for cell in df["講師"]:
#     cell = re.sub("▽", "、", cell)
#     tmp_teacher.append(cell)
# df["講師"] = tmp_teacher

# df["備考"] = "◆" + df["主催者"] + "▼□" + df["参加資格等"] + "／" + df["参加費"] + "▼■" + df["実施場所"] + "▼" + df["一時保育"]
# # 変更した内容を元のファイルへ上書き保存する。
# df.to_csv(file,
#     encoding = "utf-8",
#     index = False,
#     columns = ["日時", "単位", "内容", "備考"],
#     sep = "\t")


# for cell in df["実施日"]:
#     cell = re.sub("(\d\d?)月(\d\d?)日（([月火水木金土日])）", r"\1/\2\3", cell)
#     tmp_date.append(cell)




##### 出力
path_to_gen_file = os.path.join("./_gen", f"gene_{filename}")
df.to_csv(path_to_gen_file,
    encoding = "utf-8",
    index = False,
    columns = ["実施日", "実施時間", "単位数", "実施形態", "区分", "専門", "分野別", "研修等の名称", "講師", "主催者", "実施場所", "参加費", "参加資格等", "一時保育", "完全事前申込制"],
    sep = "\t")