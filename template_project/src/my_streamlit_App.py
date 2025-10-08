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
df_raw = load_csv("../data/raw/share-of-individuals-using-the-internet.csv")
geojson = load_json("../data/raw/countries.geojson")
df = deepcopy(df_raw)
##

st.title("Internet usage thorught the year")
st.header("data exploration")
st.table(data=df.head())
#

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