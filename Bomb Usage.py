#Requirements met
#[PY 1,3,4]
#[VIZ 1,2]
#[DA 2]


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

    #[PY1] Function with at least two uses using a default variable
def lists_to_df(lists, colNames, sortColumn, ascending = False):
    df = pd.DataFrame()
    #[PY4] List comprehension
    for i in range(0,len(lists)):
        name = str(i)
        df[name] = lists[i]
    df.columns = colNames
    #[DA2] Sort data frame
    newdf = df.sort_values(by=sortColumn, ascending=ascending)
    return newdf

file = "nuclear_explosions.csv"
nukes = pd.read_csv(file)
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
new_columns = ["Source Country", "Target", "Data Source", "Latitude", "Longitude", "magBody", "magWave", "Depth", "lowerExplosion", "upperExplosion", "Purpose", "Name", "Deployment", "Day", "Month", "Year"]
nukes.columns = new_columns
nukes["avgExplosion"] = (nukes["upperExplosion"] + nukes["lowerExplosion"])/2
st.title("Breaking Down Nuclear Explosion by Counts")
st.write("The goal of this page is to give the user an understanding of how many nuclear explosions there have been. The pie chart is focused specifically on countries throughout the years getting a grasp on who has been invovled and when. The Bar graph allows you to see the top number of nuclear explosions by any column type.")
pie = st.container(border = True)
bar = st.container(border = True)

#Pie Chart
fig1, ax1 = plt.subplots(figsize=(15,10))
pie.subheader("Piechart of all nuclear explosions by their source country")
st.sidebar.subheader("Pie Chart Filters:")
yearrange = st.sidebar.checkbox("Select a range of years?")
if yearrange:
    pieyear = st.sidebar.slider("Select a year range", nukes["Year"].min(),nukes["Year"].max(),(1950,1990))
    piestart = pieyear[0]
    pieend = pieyear[1]
else:
    piesingle = st.sidebar.slider("Select a year", nukes["Year"].min(),nukes["Year"].max())
    piestart = piesingle
    pieend = piesingle
filterDF = nukes[(nukes["Year"]>=piestart)&(nukes["Year"]<=pieend)]
countries = filterDF["Source Country"].unique()
piecounts =[]
for country in countries:
    piecounts.append(len(filterDF[filterDF["Source Country"]==country]))
piedf = lists_to_df([countries,piecounts],["Countries","Nuke Count"],"Nuke Count")
ax1.pie(piedf["Nuke Count"],labels=piedf["Countries"],autopct = lambda p: '{:.0f}'.format(p * sum(piedf["Nuke Count"]) / 100),pctdistance = .85)
    #[VIZ1] Pie Chart
pie.pyplot(fig1)


#Barchart
bar.subheader("Number of Nuclear Explosions by User Selected Filter")
st.sidebar.subheader("Bar Chart Filter")
barFilter = st.sidebar.selectbox("Select a filter",["Purpose","Deployment","Data Source","Source Country","Target"])
xVals = nukes[barFilter].unique()
fig, ax = plt.subplots(figsize=(20,10))
counts = []
for val in xVals:
    counts.append(len(nukes[nukes[barFilter]==val]))
lists = [xVals, counts]
bardf = lists_to_df(lists,["Year","Count"],"Count")
bardf.columns = [barFilter, "Counts"]
    #[PY3] error checking with try/except
try:
    num = int(st.sidebar.text_input("Enter the number of qualities"))
except:
    num = 5
ax.bar(bardf[barFilter][:num], bardf["Counts"][:num])
ax.set_xlabel(barFilter)
ax.set_ylabel("# of nuclear detonations")
    #[VIZ2] Bar Chart
bar.pyplot(fig)