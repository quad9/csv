import glob
import csv

file_path = glob.glob("./*.csv")

##### 辞書として読み込み: csv.DictReader
with open(file_path[0]) as f:
    # CSVのインスタンスを生成する。
    reader = csv.DictReader(f)
    # CSVファイルのヘッダーを配列で格納する。
    fields = reader.fieldnames
    # インスタンスreaderは、一度でもfor文で回すと
    # 元の状態を破壊されてしまうので、グローバル変数に格納する。
    rows = [row for row in reader]
    # ヘッダーに紐づいた、つまみたい項目を配列に格納する。
    head = [row[fields[1]] for row in rows]
    # つまみたい項目を配列に格納する。keyとして辞書を初期化する。
    keys = sorted(set(head), key = head.index)

    # つまみたい項目をkeyとして辞書を初期化する。
    return_dict = {}
    for row in rows:
        return_dict.setdefault(row[fields[1]], []).append(row[fields[2]])

    return_dict = { key: [] for key in keys }
    for row in rows:
        return_dict[row[fields[1]]].append(row[fields[2]])

text = ""
for k, v in return_dict.items():
    book_titles = "\n".join(v)
    contents = f"◼️{k}\n{book_titles}"
    with open("result.txt", "a") as f:
        f.write(f"{contents}\n")
