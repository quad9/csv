import os
import glob
import shutil
import jaconv
import re
import pandas as pd
import numpy as np
import sys
sys.path.append('../lib')
import t14i_regex
import t14i_string

# インデックスは、"番号", "氏名", "学年", "作・編曲者名", "演奏曲名"

###################
# 下準備

# ファイルは1枚だけが前提。
org_file = glob.glob("./_org/*.csv")[0]
filename = os.path.basename(org_file)
# create deta frame of pandas
df_in = pd.read_csv(org_file, encoding='utf-8')

# セルごとの文字列クリーニングを先にすると『NaN』が『nan』になり、
# dorpnaメソッドが効かなくなるので、不要なNaN行を先に削除処理する。
# 行のNaN,列のNaNの順番で削除する。
df_in = df_in.dropna(how='all').dropna(how='all', axis=1)

# 制作用の中間ファイルを生成させるた上で、改めてDFを生成して作業の開始。
to_tmp_file = os.path.join('./_tmp', filename)
df_in.to_csv(to_tmp_file,
    encoding = "utf-8",
    index = False,
    columns=["番号", "出演者名", "学年", "作曲者名", "編曲者名1", "編曲者名2", "演奏曲名"],
    sep = ',')

df = pd.read_csv(to_tmp_file, encoding='utf-8')

# lib/t14ireに渡してセル内の文字列を整理する。
df = t14i_regex.csv_reg(df)


###################
# df["氏名"]追加
# 編曲者名で、『本人』表記と置き換えるため

# df["出演者名"]を4文字揃えに加工してdf["氏名"]を追加する。
tmp_shimei = []
for shimei in df["出演者名"]:
    tmp_shimei.append(t14i_string.name4justify(shimei))
df["氏名"] = tmp_shimei


###################
# df["出演者名"]整理

# df["出演者名"]を7文字揃えにする。
tmp_player = []
for player in df["出演者名"]:
    tmp_player.append(t14i_string.name7justify(player))
df["出演者名"] = tmp_player


###################
# df["学年"]整理

# 学年を整理する。小学校・中学校・高校をとる。
tmp_grade = []
for grade in df["学年"]:
    res = re.search("\d", grade)
    if res == None:
        tmp_grade.append(grade)
    else:
        tmp_grade.append(grade[-2:])
df["学年"] = tmp_grade


###################
# df["作曲者名"]整理

tmp_composers = []
for line in df["作曲者名"]:
    # 全半角スペース（複数も含め）をASCIIスペースで統一してdfを整える。
    line = re.sub('\s+', ' ', line)

    # 邦人氏名の整理
    # ASCIIで構成された氏名の場合、そのまま追加する。
    if line.isascii():
        tmp_composers.append(line)
    # 邦人の場合
    else:
        # インスタンスが『/』で区切られている
        # 複数名の内容かどうかで処理の振り分け。
        res = re.search("/", line)
        if res == None:
            # 『一人の場合』
            # 空白で氏名が区切られているか。
            res = re.search("\s", line)
            if res == None:
                # スペースで区切られていなければそのまま追加。
                tmp_composers.append(line)
            else:
                # スペースで区切られていれば、4文字揃え処理をして追加。
                tmp_composers.append(t14i_string.name4justify(line))
        else:
            # 『複数名の場合』
            # 空白で氏名が区切られているか。
            tmp_names = []
            for name in line.split("/"):
                res = re.search("\s", name)
                if res == None:
                    tmp_names.append(name)
                else:
                    tmp_names.append(t14i_string.name4justify(name))
            tmp_composers.append("/".join(tmp_names))

df["作曲者名"] = tmp_composers


###################
# df["編曲者名"]整理

# df["編曲者名1"]とdf["編曲者名2"]をまとめ、字句を整理する。
tmp_arr = []
for i, arrenger in enumerate(df["編曲者名1"]):
    if df["編曲者名2"][i] is np.nan:
        tmp_arr.append(arrenger)
    else:
        tmp_arr.append(arrenger + "/" + df["編曲者名2"][i])

# 氏名を4文字揃えに整理する。
tmp_arrangers = []
for i, line in enumerate(tmp_arr):
    # 全半角スペース（複数も含め）をASCIIスペースで統一する。
    line = re.sub('\s+', ' ', line)
    tmp_names = []
    if "/" in line:
        for name in line.split("/"):
            name = name.strip()
            res = re.search("\s", name)
            # 本人名義を本人の氏名で置き換える
            if res == None:
                if "本人" in name:
                    name = df["氏名"][i]
                tmp_names.append(name)
            else:
                tmp_names.append(t14i_string.name4justify(name))
        tmp_arrangers.append("/".join(tmp_names))
    else:
        # 本人名義を本人の氏名で置き換える
        if "本人" in line:
            line = df["氏名"][i]
        tmp_arrangers.append(line)

df["編曲者名"] = tmp_arrangers


###################
# df["作・編曲者名"]追加

df["作・編曲者名"] = df["作曲者名"] + "▽" + df["編曲者名"]


###################
# df["演奏曲名"]整理
tmp_songs = []
for line in df["演奏曲名"]:
    line = re.sub('\s+', ' ', line)
    tmp_songs.append(line)
df["演奏曲名"] = tmp_songs


###################
# CSVに上書きで書き出し完成
to_gen_file = os.path.join('./_gen', filename)
df.to_csv(to_gen_file,
    encoding = "utf-8",
    index = False,
    columns=["番号", "出演者名", "学年", "作・編曲者名", "演奏曲名"],
    sep = '\t')

#####################
### オリジナルと中間ファイルを削除する。
# 検証をするときはこれらを外す。
os.remove(org_file)
os.remove(to_tmp_file)