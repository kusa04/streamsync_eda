import streamsync as ss
import plotly.express as px
import pandas as pd
import numpy as np
import os
import io

#  TODO: ファイルを選択→散布図の描画→keyerrorが発生する
# TODO: chatからmyvar２つを抽出するもっといい方法？？
# TODO: 別の変数の組み合わせを選ぶ時に毎回 "num" を打つのは煩わしい
      
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


# chatbotから数値変数を抽出する関数
def chatbot(state, payload):
    # 数値コラムのリストを作成
    num_list = ["int32", "int64", "float32", "float64"]
    df = state["df"]
    num_df_cols = df.select_dtypes(include=num_list).columns # 数値型コラムを抽出する
    state["num_df"] = df.select_dtypes(include=num_list)

    if payload == "num": # ユーザーがnumと入力したら...
        state["myvar1"], state["myvar2"] = None, None # myvar1, myvar2をNoneに初期化

        cols = [
            {
                "subheading": "Colmn",
                "name": num_df_col,
                "desc": "Click to open",
                "data": f"open_{num_df_col.split('.')[0]}",
                "result": print(f"open_{num_df_col.split('.')[0]}")
            }
            for num_df_col in num_df_cols
        ]
        
        return { # chatで返答する
            "text": "Numeric columns",
            "actions": cols
        }

    # myvar1が確定した上でmyvar2を選択する場合
    elif payload == "myvar2":
        cols = [
            {
                "subheading": "Colmn",
                "name": num_df_col,
                "desc": "Click to open",
                "data": f"open_{num_df_col.split('.')[0]}",
                "result": print(f"open_{num_df_col.split('.')[0]}")
            }
            for num_df_col in num_df_cols
        ]
        
        return { # chatで返答する
            "text": "Numeric columns",
            "actions": cols
        }

    

# chatbot内の選択肢から変数を選ぶ関数
def handle_vars_in_chatbot(state, payload):
    if payload.startswith("open_") and state["myvar1"] == None and state["myvar2"] == None:
        myvar1 = payload.split("_")[1]
        print(myvar1)
        state["myvar1"] = myvar1
        chatbot(state, "myvar2")
    
    elif payload.startswith("open_") and state["myvar1"] != None and state["myvar2"] == None:
        myvar1 = state["myvar1"]
        myvar2 = payload.split("_")[1]
        print(myvar2)
        state["myvar2"] = myvar2
        print(f"var1: {myvar1}, var2: {myvar2}")
        state["scatter"] = px.scatter(x=df.loc[:, myvar1], y=df.loc[:, myvar2], \
                         labels={"x": myvar1,"y": myvar2})






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
    "num_df": None,
    "myvar1": None,
    "myvar2": None

})

