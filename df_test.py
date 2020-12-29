import pandas as pd
import numpy as np

df = pd.read_csv('sample.csv', encoding='utf-8')

# print(df['続柄'])
# print(df.iloc[2]['続柄'])

for index, column in df.iterrows():
  if "本人" in column["続柄"]:
    column["続柄"] = column["続柄"].replace("本人", column["名前"])
    print(column["続柄"])
    print(column["名前"])
    print("yes")
  else:
    print(column["続柄"])
    print(column["名前"])
    print("no")

# print(df)

  # print(index, column["続柄"])
  
# for index, column in df.iterrows():
#   print(index, column["続柄"])

# for index, item in df.iterrows():
#   print(index, item)




# print(df.info())
# print(len(df))
# row, column = df.shape
# print(row)


# print(df.index.get_loc('john'))
# print(df.columns.get_loc('john'))

# # DataFrameの作成 ---行（index）・列（column）を指定
# arr = [[1,2,3], [4,5,6], [7,8,9]]
# org_index = ["row1", "row2", "row3"]
# colums1 = ["col1", "col2", "col3"]
# df = pd.DataFrame(data = arr, index = org_index, columns = colums1)

# print(df)

# # DataFrameの作成 ---for dict
# dict1 = dict(row1 = [1,2,3], row2 = [4,5,6], row3 = [7,8,9])
# df = pd.DataFrame(data = dict1)

# print(df)

# # DataFrameの作成 ---for number array
# arr = np.array([[1,2,3], [4,5,6], [7,8,9]])
# df = pd.DataFrame(data = arr)

# print(df)

# # DataFrameの作成 ---for string
# arr = ["john", "pual", "geroge"]
# df = pd.DataFrame(data = arr)

# print(df)



# list1 = [["P01", "nobu", "6503"],
#         ["P02", "kazu", "7106"],
#         ["P03", "mari", "9703"]]

# list2 = [["P04", "suzuki", "1111"],
#         ["P05", "honda", "2222"],
#         ["P06", "kawasaki", "3333"]]

# col1 = ["product ID", "name", "price"]

# df1 = pd.DataFrame(data = list1, columns = col1)
# df2 = pd.DataFrame(data = list2, columns = col1)

# print(df1)
# print(df2)

# ##### dfの行単位での連結・結合

# # append編

# # 書式
# # DataFrame1.append(DataFrame2, ignore_index = True/False)
# # True or Falseの違い
# # True => インデックスを新たに振り直す
# # False => 元のインデックスを生かしてリストを作る

# df3 = df1.append(df2, ignore_index = True)
# print(df3)

# # concat編

# # 書式
# # pd.concat([DataFrame1, DataFrame2, DataFrame3...],  ignore_index = True/False)
# # 利点
# # 2つ以上のdfを結合出来る。

# df4 = pd.concat([df1, df2], ignore_index = True)
# print(df4)

##### dfの列単位での連結・結合

# 内部結合 => inner join
# 外部結合 => outer join
#   左外部結合 => left outer join
#   右外部結合 => right outer join
#   完全外部結合 => full outer join

# 書式
# pd.merge(df1, df2, how = inner/left/right/outer, on = "結合キー")

# 注目している列の値と同じものをつまむ

# df_sales = [["P01", "bike", "6503"],
#          ["P02", "car", "7106"],
#          ["P03", "guitar", "1111"],
#          ["P06", "bass", "1111"],
#          ["P04", "camera", "2222"],
#          ["P07", "efector", "1111"],
#          ["P05", "piano", "9703"]]

# df_costmer = [
#          ["honda", "2222"],
#          ["yamaha", "4444"],
#          ["greco", "5555"],
#          ["suzuki", "1111"],
#          ["kawasaki", "3333"]]

# col1 = ["sales Num", "item", "customer_id"]
# col2 = ["customer_name", "customer_id"]

# df1 = pd.DataFrame(data=df_sales, columns=col1)
# df2 = pd.DataFrame(data=df_costmer, columns=col2)

# # inner
# # 同じIDのものを抽出して並べ直す
# result = pd.merge(df1, df2, how = "inner", on = "customer_id")
# print(result)
