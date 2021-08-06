import arcpy
import streamlit as st
from streamlit.elements.map import _DEFAULT_COLOR
import analysis

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


    # instantiate analysis class
    a = analysis.Analysis()

    # call input fxn
    a.input()

    # analyze button
    if st.button("Analyze!"):
        try:
            a.ras()
            a.county_analysis()
            a.total()
            a.rec()
            a.report()
            a.delete()
        except:
            # actually go in and do "except <specific error>" to be more helpful i.e. invalid state, county ...
            st.warning("Invalid inputs! Please try again")
            a.delete()