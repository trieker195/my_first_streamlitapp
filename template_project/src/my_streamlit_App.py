# Start your code here
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = 'colab'   # try changing this in case your plots aren't shown
import pandas as pd
import plotly.graph_objects as go
from urllib.request import urlopen
from plotly.subplots import make_subplots
import json
from copy import deepcopy

# functions
@st.cache_data
def load_csv(path):
        df=pd.read_csv(path)
        return df

@st.cache_data
def load_json(path):
        with open(path) as f:
            geojson = json.load(f)
        return geojson
####

#load in data
df_internet = load_csv("template_project/data/raw/share-of-individuals-using-the-internet.csv")
df_socioeco = px.data.gapminder()
geojson = load_json("template_project/data/raw/countries.geojson")

#rename columns to merge by country code and year
df_socioeco = df_socioeco.rename(columns={"iso_alpha": "Code","year":"Year","country":"Country"})
df_internet = df_internet.rename(columns={"Entity": "Country","year":"Year"})
#merge df by code and year
df_merged = df_internet.merge(df_socioeco,on=["Code","Year","Country"],how="inner")

#group by conteninten
df_mean_cont =  df_merged.groupby(["continent","Year"])[["gdpPercap","Individuals using the Internet (% of population)","lifeExp","pop"]].mean()

df = deepcopy(df_merged)
##

st.title("Internet usage thorught the year")
st.header("data exploration")
#st.table(data=df.head())
#

# checkbox dataframe
if st.sidebar.checkbox("dispay/hide"):
       st.header("dataframe")
       st.dataframe(df.head())


# chose year button
years = sorted(df["Year"].unique())
year = st.selectbox("chose year",years)
#df_new = df[df["Year"].isin(range(1990,2021))]
df_new = df[df["Year"]== year]


#plot
fig = px.choropleth(data_frame=df_new, geojson=geojson, locations="Code", featureidkey="properties.ISO_A3",
                    color="Individuals using the Internet (% of population)",
                    color_continuous_scale="Viridis",
                    animation_frame="Year")
fig.update_layout(title="(%) of population using Internet throughout the years")

st.plotly_chart(fig)

###



st.header("relationship between different catgeories")
# chose categ button
categories = ["gdpPercap","Individuals using the Internet (% of population)","lifeExp","pop"]
category1 = st.selectbox("chose category",categories, key="cat1")

# chose categ button
category2 = st.selectbox("chose category",categories, key="cat2")


#scatterplot
# get unique continetn names
unique_conts = df_mean_cont.index.get_level_values(0).unique().to_list()

#plot
fig2 = go.Figure()
for cont in unique_conts:
    df_cont = df_mean_cont.loc[cont]
    fig2.add_trace(go.Scatter(x=df_cont[category1],
                             y=df_cont[category2],
                             name=cont,
                            ))

# hover 
fig2.update_layout(hovermode="x unified",
                 paper_bgcolor="lightgray",
                 plot_bgcolor="white",
                 title=f"relationship between {category1} and {category2} [years 1992-2007]",
                 xaxis_title=category1,
                 yaxis_title=category2,
                 xaxis_title_font=dict(size=18),
                 yaxis_title_font=dict(size=18),
                 )

st.plotly_chart(fig2)
