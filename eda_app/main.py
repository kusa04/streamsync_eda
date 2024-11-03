import streamsync as ss
import plotly.express as px
import pandas as pd

# TODO: file読み込みからdfを表示できるようにする
#  TODO: 動的にグラフの描画

def select_csv(state, payload):
    state["csv_name"] = payload
    print(f"csv_name: {state['csv_name']}")
    state["df"] = pd.read_csv(f"static/{state['csv_name']}")
    df = state["df"]
    
def onchange_handler(state, payload):

	# Set the state variable "selected" to the selected option

	state["selected"] = payload


df = "/static/covid_flu.csv"


initial_state = ss.init_state({

    "initial_csv": pd.read_csv("static/covid_flu.csv"),
    "df": df,
    "csv_name": ""

})

