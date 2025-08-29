# Data_Clean

Raw data from system--bonus query--export

Problem with raw data: Duplicates in Recharge amount column(充值金额) 
How to Solve:

1. Load the data
Reads the CSV file from your Desktop using GBK encoding into a DataFrame named df.

2. Define which amounts can be “monthly packages”
Creates a set {11000, 11500, 17000, 23000, 38000} to identify the amounts that can appear duplicated.

3. Split the data into two parts
df_need: rows where the dormancy (休眠时长) ≥ 31 days and the amount (充值金额) is in the monthly set.
These are the rows that may have duplicates and need cleaning.
df_other: all remaining rows (not in the above condition) that should stay as-is.

4. Clean duplicates within the “need to clean” subset
Groups df_need by Smart Card Number (智能卡号) + Amount (充值金额) + Dormancy (休眠时长).
For each group:
  Sums the commission column (增加/减少数量) so two records like 550 + 550 become 1100.
  For all other columns, keeps the first value in that group.

5. Combine back
Concatenates the cleaned part (df_cleaned) with the untouched part (df_other) to form final_df.

6. Save the result
Writes final_df to an Excel file on your Desktop: 07月清洗以后去重版.xlsx.


# Data_Reorganize
1. **Load input file**
   * Reads `07月清洗以后去重版.xlsx` from the desktop into a pandas DataFrame (`df`).

2. **Define the “monthly-package” amounts**
   * `MONTHLY_AMOUNTS = {11000, 11500, 17000, 23000, 38000}`
     These values flag a recharge as a *monthly package*.

3. **Convert key columns to numeric**
   * Ensures `充值金额`, `休眠时长`, and `增加/减少数量` are numeric; non-numeric values become 0.

4. **Filter for the target business operation**
   * Keeps only rows where `业务操作` equals **“休眠唤醒”**.

5. **Create dormancy buckets**
   * Maps `休眠时长` to five text ranges:
     `1-30`, `31-90`, `91-180`, `181-360`, `>360`.

6. **Flag monthly vs. non-monthly**
   * New column `是否月包` is **True** if `充值金额` is in `MONTHLY_AMOUNTS`, otherwise **False**.

7. **Aggregate totals**
   * Groups by `员工编码`, `员工名称`, `休眠区间`, and `是否月包`;
     computes **sum of 充值金额** and **sum of 增加/减少数量 (commission)**.

8. **Sort results**
   * Orders by employee and the logical sequence of the five dormancy buckets.

9. **Split into two DataFrames**
   * `df_monthly`  → rows where `是否月包` == True.
   * `df_nonmonthly` → rows where `是否月包` == False.
   * Drops the indicator column afterwards.

10. **Export results**
    * Writes `df_monthly` to `07月_休眠唤醒_月包汇总.xlsx`.
    * Writes `df_nonmonthly` to `07月_休眠唤醒_非月包汇总.xlsx`.
