import arcpy
import streamlit as st
from streamlit.elements.map import _DEFAULT_COLOR
import analysis
import os

def main():
    # set env
    # path/workspace might be an issue for production
    # also this is a brutal way of changing dirs...
    os.chdir("..")
    os.chdir("..")
    os.chdir("..")
    os.chdir("GIS")
    arcpy.env.workspace = f"{os.getcwd()}\AgroPV"
    os.chdir("..")
    os.chdir("Python")
    os.chdir("duo-tool")
    os.chdir("app")
    done = []

    # app header/title
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Arup_Red_RGB.png", width = 100)
    st.write('''
    # Dual Land Use - AgroPV Tool
    ''')
    st.markdown('''
    ## Welcome! Enter a State and County, and the coresponding Lat, Lon coordinates for that location
    ''')

    # sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Enel_Group_logo.svg/1200px-Enel_Group_logo.svg.png", width=130)
    st.sidebar.write('''
    ## Welcome to the Dual Use Opportunities Tool (DUO), developed in partnership between Enel and Arup

    # Intro

    ...

    # Layers background

    **Cattle Production**: Number of cattle operations with sales in 2017, categorized by county. Data from the Census of Agriculture, produced by the USDA National Agricultural Statistics Service

    **Sheep and Lamb**: Average number of sheep and lambs per 100 acres of all farmland in 2012. Data from the Census of Agriculture, produced by the USDA National Agricultural Statistics Service

    ...

    # Etc

    ...

    ''')


    # instantiate analysis class
    a = analysis.Analysis()

    # call input fxn
    a.input()

    # analyze and download button
    if st.button("Analyze and Download Report"):
        try:
            a.ras()
            a.county_analysis()
            a.total()
            a.delete()
            done = 1
            if done==1: # add actual logic
                a.report("Grazers-Pollinators")
        except:
            # actually go in and do "except <specific error>" to be more helpful i.e. invalid state, county ...
            st.warning("Invalid inputs! Please try again")
            a.delete()