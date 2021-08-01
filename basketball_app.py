import pandas as pd
import urllib.request as req
import streamlit as st


# 變寬
st.set_page_config(layout="wide")

# 選擇例行賽還是季後賽
option = ["例行賽", "季後挑戰賽"]
seasons=st.sidebar.selectbox("例行賽",option)

# 讀取 CSV 資料
@st.cache
def getData(seasons):
    if(seasons == option[0]):
        playerstats=pd.read_csv("regularseason.csv")
    if(seasons == option[1]):
        playerstats=pd.read_csv("playoffs.csv")
    return playerstats

playerstats = getData(seasons)

# 標題
if(seasons == option[0]):
    st.markdown("""
    # P.League+ Players Stats 
    (Regular Season)
    """)
else:
    st.markdown("""
    # P.League+ Players Stats 
    (Post Season)
    """)

st.dataframe(playerstats)

# 球隊
sorted_teams=sorted(playerstats["球隊"].unique())
selected_teams=st.sidebar.multiselect("球隊", sorted_teams, sorted_teams)

# 排序方式
ordertitle=playerstats.drop(columns=["球員", "背號"])
sorted_order=sorted(ordertitle)
selected_order=st.sidebar.selectbox("排序方式", sorted_order)

# 球員姓名
title = st.sidebar.text_input('搜尋球員姓名')

# filtering data

df_selected_team_and_order = playerstats[(playerstats["球隊"].isin(selected_teams))]
st.header('Display Player Stats of Selected Team(s) & Selected Order')
st.write('Data Dimension: ' + str(df_selected_team_and_order.shape[0]) + ' rows and ' + str(df_selected_team_and_order.shape[1]) + ' columns.')
st.dataframe(df_selected_team_and_order.sort_values(by=selected_order, ascending=False))

names = pd.Series(title)
names = sorted(names)
pattern = '|'.join(names)
df=playerstats[playerstats["球員"].str.contains(pattern)]
if len(title)!=0:
    if(playerstats["球員"].str.contains(pattern).any()): # .any() 有任何球員名稱符合時，回傳 True
        st.header("Display Player Stats of Specific Player(s)")
        st.dataframe(df)
    else:
        st.write("Players Not Found")
