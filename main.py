import pandas as pd
from obs import PutObjectHeader
from obs import HeadPermission
import sys
from obs import ObsClient
import plotly.graph_objects as go
import plotly.subplots as sp
from datetime import datetime
import os
from jinja2 import Template
import numpy as np
from datetime import timedelta
from datetime import datetime
import docx
import os
from pydocx import PyDocX
import zipfile
from pyecharts.charts import HeatMap
from pyecharts import options as opts
import numpy as np
import math
import plotly.express as px
import pandas as pd
def bins(start,end,step):
    result = []
    i = start
    while i < end:
        result.append(i)
        i += step
    return result
data=pd.read_excel("data/1865_0105_0106.xlsx")
data['瞬时电机输出功率(KW)']=4*data['MCUSpeed"rpm"']*((data['MCUPercentTorque"%"']
                                                     +0.125*data['HighResolutionMCUTorque'])/100)*2500/9550
count=data['瞬时电机输出功率(KW)'].count()
print("max&min")
print(data['瞬时电机输出功率(KW)'].min())
print(data['瞬时电机输出功率(KW)'].max())
df=data
speed_bins = list(range(0, 151, 5))
power_bins = list(range(-2000, 2000, 10))
df['Speed Range'] = pd.cut(df['WheelBasedVehicleSpeed(1)"kmPh"'], bins=speed_bins)
df['Power Range'] = pd.cut(df['瞬时电机输出功率(KW)'], bins=power_bins)
heatmap_data = df.groupby(['Power Range', 'Speed Range']).size().unstack().fillna(0)
heatmap_data = (heatmap_data / count * 100).round(3)
# heatmap_percentage = heatmap_data.apply(lambda x: x*100 / x.sum(), axis=0).fillna(0)
# print(heatmap_data)
heatmap_data_list = heatmap_data.values.tolist()
# print(heatmap_data_list)
# fig = go.Figure(data=go.Heatmap(z=heatmap_data_list))
# fig.show()
total_sum = heatmap_data.sum()

# print("所有组的总和:")
# print(total_sum)
trace = go.Heatmap(
    # xgap=1,  # 控制 x 轴刻度线间隔
    # ygap=1,  # 控制 y 轴刻度线间隔
    y=power_bins,
    x=speed_bins,
    z=heatmap_data,
    colorscale='Jet',
    hovertemplate = "车速(KM/H): %{x}<br>功率(KW): %{y}<br>所占百分比(%): %{z}<extra></extra>",
)

# 创建图表布局
layout = go.Layout(
    title='基于电机输出功率与车速的热力图',
    yaxis=dict(title='电机输出功率范围(KW)'),
    xaxis=dict(title='车速范围(KM/H)'),
)

# 绘制热力图
fig = go.Figure(data=[trace], layout=layout)

# 显示图表
fig.show()

df['坡度'] = df['计算坡度'].apply(lambda x: math.degrees(math.atan(x/100)))
start = -10
end = 10
step = 0.005

result = []
i = start
while i < end:
    result.append(i)
    i += step
# result=[-20,-15,-10,-8,-6,-5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,]
podu_bins =result
power_bins = list(range(-2000, 2000, 10))
df['Podu Range'] = pd.cut(df['坡度'], bins=podu_bins)
df['Power Range'] = pd.cut(df['瞬时电机输出功率(KW)'], bins=power_bins)
heatmap_data = df.groupby(['Power Range', 'Podu Range']).size().unstack().fillna(0)
heatmap_data = (heatmap_data / count * 100).round(3)
heatmap_data_list = heatmap_data.values.tolist()
trace = go.Heatmap(
    # xgap=1,  # 控制 x 轴刻度线间隔
    # ygap=1,  # 控制 y 轴刻度线间隔
    y=power_bins,
    x=podu_bins,
    z=heatmap_data,
    colorscale='Jet',
    hovertemplate = "坡度(°): %{x}<br>功率(KW): %{y}<br>所占百分比(%): %{z}<extra></extra>",
)

# 创建图表布局
layout = go.Layout(
    title='基于坡度与电机输出功率的热力图',
    yaxis=dict(title='电机输出功率范围(KW)'),
    xaxis=dict(title='坡度范围(°)'),
)

# 绘制热力图
fig1 = go.Figure(data=[trace], layout=layout)

# 显示图表
fig1.show()



# 使用 plotly 绘制直方图
fig = px.histogram(df, x='坡度', nbins=60, histnorm='probability')

# 设置图表坐标轴标签和标题
fig.update_layout(
    xaxis_title='坡度（度）',
    yaxis_title='占比 (%)',
    title='坡度分布图'
)

# 格式化y轴标签为百分比形式
fig.update_yaxes(tickformat=".2%")

fig.show()
# 显示图表