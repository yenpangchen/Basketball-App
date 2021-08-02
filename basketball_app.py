import pandas as pd
import urllib.request as req
import streamlit as st


# 變寬
st.set_page_config(layout="wide")

# 選擇例行賽還是季後賽
option = ["例行賽", "季後挑戰賽"]
seasontype=st.sidebar.selectbox("例行賽",option)

# 爬蟲抓資料
@st.cache
def getData(seasontype):
    if(seasontype == option[0]):
        playerstats=pd.read_csv("regularseason.csv")
    if(seasontype == option[1]):
        playerstats=pd.read_csv("playoffs.csv")
    return playerstats

playerstats = getData(seasontype)

# 標題
if(seasontype == option[0]):
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

# 更正三分%因為是 str 所以會有排序錯誤的問題
def sort_values_by_selected_order(df, selected_order):
    df=df.replace('%',"",regex=True)
    df[["兩分%", "三分%", "罰球%"]]=df[["兩分%", "三分%", "罰球%"]].astype('float64')
    df=df.sort_values(by=selected_order, ascending=False)
    df[["兩分%", "三分%", "罰球%"]]=df[["兩分%", "三分%", "罰球%"]].astype('str')
    df[["兩分%", "三分%", "罰球%"]]=df[["兩分%", "三分%", "罰球%"]]+"%"
    return df

# filtering data

df_selected_team_and_order = playerstats[(playerstats["球隊"].isin(selected_teams))]
st.header('Display Player Stats of Selected Team(s) & Selected Order')
st.write('Data Dimension: ' + str(df_selected_team_and_order.shape[0]) + ' rows and ' + str(df_selected_team_and_order.shape[1]) + ' columns.')
st.dataframe(sort_values_by_selected_order(df_selected_team_and_order, selected_order))

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

