import pandas as pd
# 读取 Excel 文件
df = pd.read_excel('pm.xlsx')
# 数据处理
df_grouped = df.groupby('ProjectName')['Owner'].agg(lambda x: ','.join(x)).reset_index()
# 输出结果
df_grouped.to_excel('output.xlsx', index=False)