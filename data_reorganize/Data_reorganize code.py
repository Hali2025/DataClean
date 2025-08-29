import pandas as pd
import numpy as np

# 路径
src_file = r"C:\Users\26251\Desktop\07月清洗以后去重版.xlsx"
out_file_monthly    = r"C:\Users\26251\Desktop\07月_休眠唤醒_月包汇总.xlsx"
out_file_nonmonthly = r"C:\Users\26251\Desktop\07月_休眠唤醒_非月包汇总.xlsx"

# 读取
df = pd.read_excel(src_file)

# 月包金额集合
MONTHLY_AMOUNTS = {11000, 11500, 17000, 23000, 38000}

# 数值化
for col in ["充值金额", "休眠时长", "增加/减少数量"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# 仅保留“休眠唤醒”
df = df[df["业务操作"] == "休眠唤醒"].copy()

# 区间函数（五档：1-30 / 31-90 / 91-180 / 181-360 / >360）
def dorm_bucket(days):
    if pd.isna(days): 
        return ">360"
    d = int(days)
    if d <= 30:    return "1-30"
    elif d <= 90:  return "31-90"
    elif d <= 180: return "91-180"
    elif d <= 360: return "181-360"
    else:          return ">360"

df["休眠区间"] = df["休眠时长"].apply(dorm_bucket)

# 标记是否月包（按金额集合）
df["是否月包"] = df["充值金额"].isin(MONTHLY_AMOUNTS)

# 分组汇总（员工编码、员工名称、休眠区间、是否月包）
agg_df = (df.groupby(["员工编码", "员工名称", "休眠区间", "是否月包"], as_index=False)
            .agg(充值金额合计=("充值金额", "sum"),
                 提成金额合计=("增加/减少数量", "sum")))

# 排序（可选）
order_map = {"1-30": 1, "31-90": 2, "91-180": 3, "181-360": 4, ">360": 5}
agg_df["区间顺序"] = agg_df["休眠区间"].map(order_map)
agg_df = agg_df.sort_values(["员工编码", "员工名称", "区间顺序"]).drop(columns="区间顺序")

# 拆分导出：月包 / 非月包
df_monthly    = agg_df[agg_df["是否月包"]  == True ].copy()
df_nonmonthly = agg_df[agg_df["是否月包"]  == False].copy()

# 去掉“是否月包”列（可保留也行，看你偏好）
df_monthly.drop(columns=["是否月包"], inplace=True)
df_nonmonthly.drop(columns=["是否月包"], inplace=True)

# 导出
df_monthly.to_excel(out_file_monthly, index=False)
df_nonmonthly.to_excel(out_file_nonmonthly, index=False)

print("导出完成：")
print(out_file_monthly)
print(out_file_nonmonthly)

