"""
Name:   Nathaniel Post
CS230:  Section 5
Data:   Nuclear Explosions 1945-1998
URL:    ###

Descriprion:

This program uses a data set of nuclear explosions from the very first test in 1945 to 1999.
In the progam after some basic data manipulation, I created a streamlit web page to display the
data in a number of different graphs and charts. The goal was not to reveal a specific point but to
give the user an idea of the development and use of nuclear weapons of the years and the scale
at which it was done. please enjoy.

Extra Credit:

To better format by streamlit page I used the streamlit columns and containers functions.
"""
#Requirements met
#[ST 1,2,3,4]
#[DA 1,4,9]

import pandas as pd
import streamlit as st


file = "nuclear_explosions.csv"
nukes = pd.read_csv(file)
pd.set_option("display.max_rows", None, "display.max_columns", None, 'display.width', None, 'max_colwidth', None)
new_columns = ["Source Country", "Target", "Data Source", "Latitude", "Longitude", "magBody", "magWave", "Depth", "lowerExplosion", "upperExplosion", "Purpose", "Name", "Deployment", "Day", "Month", "Year"]
    #[DA1] Clean or manipulate data
nukes.columns = new_columns
    #[DA9]Added a new Column and did calculation
nukes["avgExplosion"] = (nukes["upperExplosion"] + nukes["lowerExplosion"])/2
st.title("Data Visualization using Python and Streamlit")
st.write("This is data showing all known nuclear explosions compiled and displyed by Nathaniel Post")

def country_Summary(df, country):
    data = {"Country": country}
    bombNum = len(df[df["Source Country"] == country])
    Largest = str(round(df[df["Source Country"] == country]["avgExplosion"].max(),2))
    avgBomb = str(round(df[df["Source Country"] == country]["avgExplosion"].mean(),2))
    return bombNum, Largest, avgBomb

    #Main Data representation and filtering
mainData = st.container(border = True)
mainData.subheader("Full Data Set")
st.sidebar.subheader("Main Data Set")
    #[ST1] Checkbox
filter = st.sidebar.checkbox("Filter")
if filter:
    #[ST2] Selectbox
    mainFilter = st.sidebar.selectbox("Select a column to filter by",["Source Country","Target","Data Source","Purpose","Deployment","Year"])
    uniqueVals = nukes[mainFilter].unique()
    filterVal = st.sidebar.multiselect("Select a value",uniqueVals)
    #[DA4] Filter data by one condition
    mainData.write(nukes[nukes[mainFilter].isin(filterVal)])
else:
    mainData.write(nukes)

    #Country Summary
st.sidebar.subheader("Country Summary")
country = st.sidebar.selectbox("Select a country",nukes["Source Country"].unique())
factsList = country_Summary(nukes,country)
    #[ST3-4] Containers and Columns
c = st.container(border = True)
total, max, avg = st.columns(3,border = True)
c.subheader("Country Summary")
c.write(country)
total.metric("Total Nuclear Bomb Explosions",factsList[0])
max.metric("Largest Caused Explosion", factsList[1])
avg.metric("Average Nuclear Bomb Size",factsList[2])



