#Requirements met
#[VIZ 3]


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def lists_to_df(lists, colNames, sortColumn, ascending = False):
    df = pd.DataFrame()
    for i in range(0,len(lists)):
        name = str(i)
        df[name] = lists[i]
    df.columns = colNames
    newdf = df.sort_values(by=sortColumn, ascending=ascending)
    return newdf

file = "nuclear_explosions.csv"
nukes = pd.read_csv(file)
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
new_columns = ["Source Country", "Target", "Data Source", "Latitude", "Longitude", "magBody", "magWave", "Depth", "lowerExplosion", "upperExplosion", "Purpose", "Name", "Deployment", "Day", "Month", "Year"]
nukes.columns = new_columns
nukes["avgExplosion"] = (nukes["upperExplosion"] + nukes["lowerExplosion"])/2
st.title("Understanding Development of Nuclear Explosions over the years")
st.write("The goal of this page is to get an idea of how the size and magnitude of nuclear explosions have changed over the years.")

#Linecharts
c = st.container(border = True)
years = nukes["Year"].unique()
lower = []
upper = []
body = []
surface = []
for year in years:
    lower.append(nukes[nukes["Year"] == year]["lowerExplosion"].mean())
    upper.append(nukes[nukes["Year"] == year]["upperExplosion"].mean())
    body.append(nukes[nukes["Year"] == year]["magBody"].mean())
    surface.append(nukes[nukes["Year"] == year]["magWave"].mean())
lists = [years, lower, upper, body, surface]
linedf = lists_to_df(lists,["Year","lowerExplosion","upperExplosion","magBody","magWave"],"Year",True)
st.sidebar.subheader("Line Graph Filter:")
whichGraph = st.sidebar.radio("Filter", ["Explosion Size","Explosion Magnitude"])
c.subheader("Line Graph of " + str(whichGraph) + " Over the Years")
fig, ax = plt.subplots()
if whichGraph == "Explosion Size":
    ax.plot(linedf["Year"],linedf[["lowerExplosion","upperExplosion"]], marker = "o")
    ax.legend(["Lower Limit","Upper Limit"])
    ax.set_ylabel("Average Explosion Esitmate in Kilotons of TNT")
else:
    ax.plot(linedf["Year"], linedf[["magBody", "magWave"]])
    ax.legend(["Body Wave Magnitude","Surface Wave Magnitude"])
    ax.set_ylabel("Average Explosion Magnitudes (mb)")
    #[VIZ3] Line Chart
ax.set_xlabel("Years")
c.pyplot(fig)