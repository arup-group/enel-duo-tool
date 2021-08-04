# import modules and get license
import pandas as pd
import arcpy
import streamlit as st
from streamlit.elements.map import _DEFAULT_COLOR
import analysis
from SessionState import get # for login
import os


def main():
    # set env
    # path/workspace might be an issue for production 
    arcpy.env.workspace = r"C:\Users\alden.summerville\OneDrive - Arup\AgroPV Tool\GIS\AgroPV"

    # app header/title
    st.write('''
    # Dual Land Use - AgroPV Tool
    ''')
    st.markdown('''
    ## Welcome! Enter ....instructions and background
    ''')

    # sidebar
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Enel_Group_logo.svg/1200px-Enel_Group_logo.svg.png", width=130)
    st.sidebar.write('''
    ## Welcome to the Enel Dual Land Use (DUO) AgroPV tool developed by Arup....

    # Intro

    ...

    # Layers background

    ...

    # Etc

    ...

    ''')

    # ask user for input
    # add some error handling
    state = st.text_input("State: ")
    county = st.text_input("County: ")
    st.write('''
    Get lon, lat coordinates from an address [here](https://www.latlong.net/)
    ''')
    lat = st.text_input("Latitude: ")
    lon = st.text_input("Longitude: ")

    # set variables for testing
    # lon = -75.57281
    # lat = 39.147316
    # state = 'Delaware'
    # county = 'Kent'


    # instantiate class
    a = analysis.Analysis()

    # analyze button
    if st.button("Analyze!"):
        a.ras()
        a.county()
        a.total()
        a.rec()
        a.delete()

# login:

session_state = get(password='')

if session_state.password != os.getenv("enelpassword"):
    pwd_placeholder = st.sidebar.empty()
    pwd = pwd_placeholder.text_input("Password:", value="", type="password")
    session_state.password = pwd
    if session_state.password == os.getenv("enelpassword"):
        pwd_placeholder.empty()
        main()
    elif session_state.password != '':
        st.error("the password you entered is incorrect")
else:
    main()