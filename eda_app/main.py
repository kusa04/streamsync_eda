import streamsync as ss
import plotly.express as px
import pandas as pd
import numpy as np
import os
import io

#  TODO: 動的にグラフの描画
      
# 選択したファイルをstate["df"]に格納する関数     
def load_csv_file(state, payload):
    # リストの最初の要素からファイルデータを取得
    uploaded_file = payload[0]
    file_data = uploaded_file.get("data")  # ファイルデータ（バイナリ形式）
    
    # バイナリデータをバッファとして扱う
    file_buffer = io.BytesIO(file_data)
    
    # pd.read_csvでバッファから読み込む
    state["df"] = pd.read_csv(file_buffer)
    df = state["df"]
    print(df.head())
    # state["numeric"] = df.select_dtypes(include=[np.number])
    # state["category"]




# 散布図描画
def scatter_plot(state, payload):
    var1, var2 = payload





############# 各値の初期化 #############

df = pd.read_csv("static/covid_flu.csv")
scatter = px.scatter(x=df.loc[:, "Age"], y=df.loc[:, "Temperature"], \
                     color=df.loc[:, "Sex"], labels={
                         "x": "Age",
                         "y": "Temperature"
                     })



initial_state = ss.init_state({

    "df": df,
    "scatter": scatter,
    "numeric": None,

})

