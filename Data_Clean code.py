import pandas as pd

# 路径
src_file = r"C:\Users\26251\Desktop\07_20250828105826.csv"
out_file = r"C:\Users\26251\Desktop\07月清洗以后去重版.xlsx"

# 读取源数据
df = pd.read_csv(src_file, encoding="gbk")

# 月包金额集合
monthly_packages = {11000, 11500, 17000, 23000, 38000}

# 拆分需要处理的和不需要处理的
df_need = df[(df["休眠时长"] >= 31) & (df["充值金额"].isin(monthly_packages))]
df_other = df[~((df["休眠时长"] >= 31) & (df["充值金额"].isin(monthly_packages)))]

# 对需要处理的部分：按照智能卡号+充值金额+休眠时长等关键字段去重，并合并提成
agg_cols = {col: "first" for col in df_need.columns}
agg_cols["增加/减少数量"] = "sum"   # 提成相加

df_cleaned = df_need.groupby(
    ["智能卡号", "充值金额", "休眠时长"], as_index=False
).agg(agg_cols)

# 合并结果
final_df = pd.concat([df_other, df_cleaned], ignore_index=True)

# 保存
final_df.to_excel(out_file, index=False)

print("清洗完成，文件已保存到：", out_file)


