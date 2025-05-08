#Requirements met
#[PY 5]
#[DA 3,5]
#[MAP]

import pandas as pd
import streamlit as st

file = "nuclear_explosions.csv"
nukes = pd.read_csv(file)
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
new_columns = ["Source Country", "Target", "Data Source", "Latitude", "Longitude", "magBody", "magWave", "Depth", "lowerExplosion", "upperExplosion", "Purpose", "Name", "Deployment", "Day", "Month", "Year"]
nukes.columns = new_columns
nukes["avgExplosion"] = (nukes["upperExplosion"] + nukes["lowerExplosion"])/2
st.title("Geographic Breakdown of Nuclear Explosions")
st.write("This map shows the locations of all nuclear explosions within a selected time range. On the map itself each dot is colored based on its source country and size based on its explosion size.")

#Link for Colors: http://colormind.io/
    #[PY5] Dictionary used to set colors
colorByCountry = {"USA":"#0068c9",
                  "USSR":"#ff2b2b",
                  "UK":"#262730",
                  "FRANCE":"#09ab3b",
                  "CHINA":"#eaf000",
                  "INDIA":"#dc671d",
                  "PAKIST":"#dc1dbb"}
colorCol = []
for i in range(0,len(nukes["Source Country"])):
    colorCol.append(colorByCountry[nukes.iloc[i,0]])
nukesMap = nukes
nukesMap["Color"] = colorCol
    #[DA3] Find largest or smallest values of a column
min = nukes["Year"].min()
max = nukes["Year"].max()
    #[ST5] Slider
years = st.slider("Select a year range",min,max,(1955,1990))

key,map = st.columns([.2,.8],vertical_alignment="top")
    #[MAP]
    #[DA5] Filter Data Frame by two or more variables
with map:
    st.map(nukes[(nukesMap["Year"]>=years[0])&(nukes["Year"]<=years[1])],latitude = "Latitude",longitude = "Longitude",color = "Color",size = "upperExplosion")
colorByCountryReadable = {"Countries":nukesMap["Source Country"].unique(),"Colors":["Blue","Red","Black","Green","Yellow","Orange","Pink"]}
colorsdf = pd.DataFrame(colorByCountryReadable,index = ['level 1','level 2','level 3','level 4','level 5','level 6','level 7'])
df = colorsdf.set_index("Countries", inplace=True)
with key:
    st.subheader("Key")
    st.write(colorsdf)