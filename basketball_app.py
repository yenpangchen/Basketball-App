import pandas as pd
import urllib.request as req
import streamlit as st

# 變寬
st.set_page_config(layout="wide")

# 爬蟲抓資料
@st.cache
def getData():
    url="http://pleagueofficial.com/stat-player"
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    df=pd.read_html(data)
    playerstats=df[0]
    return playerstats

playerstats = getData()

st.markdown("""
# P.League+ Players Stats 
(Regular Season)
""")

st.dataframe(playerstats)
#st.write(playerstats.columns)

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
if(playerstats["球員"].str.contains(pattern).any()): # .any() 有任何球員名稱符合時，回傳 True
    st.header("Display Player Stats of Specific Player")
    st.dataframe(df)
