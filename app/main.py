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
    ## Welcome! Enter a State and County, and the corresponding Lat, Lon coordinates for that location
    ''')

    # sidebar
    # probably should create a dropdown for the layers background cause it's a huge section (don't want them pre-expanded)
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Enel_Group_logo.svg/1200px-Enel_Group_logo.svg.png", width=130)
    st.sidebar.write('''
    ## Welcome to the Dual Use Opportunities Tool (DUO), developed in partnership between Enel and Arup

    # Intro

    ...

    # Layers background

    **Sheep & lambs per 100 acres**: Average number of sheep and lambs per 100 acres of all US farmland in 2012. Data is from the National Agricultural Statistics Service (NASS). This will help us determine if there is local viability for sheep and expertise already in the area.

    **Crop type**: Primary crop grown during every growing season in the US since 2008. Data is from the USDA CropScape Cropland Data Layers from the National Agricultural Statistics Service (NASS). This will help us distinguish the dominant agricultural product in the local market.

    **Crop sales (USDA)**: Crop sales in US Dollars in 2017. Data is from the Census of Agriculture, produced by the USDA National Agricultural Statistics Service. This will help us understand the financial potential of the local agricultural market.

    **Commodity Crop Productivity Index**: The National Commodity Crop Productivity Index (NCCPI) ranks the inherent capability of soils to produce agricultural crops without irrigation on a scale of zero to one. Data is from the USDA Gridded National Soil Survey Geographic Database (gNATSGO). This will give us insight on soil conditions and health, helping us determine which crops would be most suitable for the site. 

    **Rainfall**: Average precipitation, quantified in milimeters per month. Data is from WorldClim at 2.5 minutes resolution. This will give us an understanding about rainfall in the area, whether there is an abundance or a scarcity, helping us determine which crops would be most suitable for the site. 

    **Number of imperiled vertebrate species**: Numbers of vertebrate species that are protected by the Endangered Species Act and/or considered to be in danger of extinction in the US, updated April 2021. Data is from the Map of Biodiversity Importance (MoBI) data collection, a series of maps that identify areas of high importance to focus biodiversity protection efforts. The data consisting of 309 species, including birds, mammals, amphibians, reptiles, freshwater fishes. This will provide valuable information on species we will want to take action to protect.

    **Number of imperiled pollinator species**: Numbers of pollinator species that are protected by the Endangered Species Act and/or considered to be in danger of extinction in the US, updated April 2021. Data is from the Map of Biodiversity Importance (MoBI) data collection, a series of maps that identify areas of high importance consisting of 42 species, including bumblebees, butterflies, and skippers. This will provide valuable information on pollinator species we will want to take action to protect, and thus inform the pollinator-attracting species specified onsite.

    **Number of imperiled vascular plant species**: Numbers of vascular plant species that are protected by the Endangered Species Act and/or considered to be in danger of extinction in the US, updated April 2021. Data is from the Map of Biodiversity Importance (MoBI) data collection, a series of maps that identify areas of high importance consisting of 309 species, including all plants that have a vascular system, in other words, every plant except algea, mosses, liverhorts, and hornworts. This will provide valuable information on plant species we will want to take action to protect, guiding specifications on which plants to grow onsite and which need to be avoided.

    **Land use type**: Land uses, including: Open Water, Perennial Ice/Snow, Developed Open Space, Developed Low Intensity, Developed Medium Intensity, Developed High Intensity, Barren Land, Deciduous Forest, Evergreen Forest, Mixed Forest, Dwarf Scrub, Shrub/Scrub, Grassland/Herbaceous, Sedge/Herbaceous, Lichens, Moss, Planted/Cultivated, Pasture/Hay, Cultivated Crops, Woody Wetlands, Emergent Herbaceous Wetlands. This will give us an understanding of historical land use of the site, its potential, and conditions. 

    **National Risk Index (NRI) Score**: Normalized Risk Index score is calculated from Social Vulnerability, Community Resilience, and Expected Annual Loss, which is derived from multiplying hazard exposure, frequency, and historical losses. Risks include Avalanche, Coastal Flooding, Cold Wave, Drought, Earthquake, Hail, Heat Wave, Hurricane, Ice Storm, Landslide, Lightning, Riverine Flooding, Strong Wind, Tornado, Tsunami, Volcanic Activity, Wildfire, and Winter Weather. Data is calculated at the county and census tract levels, pulled from a long list of accredited sources inlcuding universities and government agencies, and most recently updated in October 2020. This will help us understand what risks to design for and what scenario planning should be done.

    **Topography**: Groud surface heights provide correlated slope values, given in percentage. Data is from the NED 1 arc-second dataset in the USGS's National Elevation Dataset program. This will help us determine what type of solar and agriculture make sense onsite.

    **Sunlight - Solar power potential**: The solar power generation potential for a photovoltaic system per capacity built, called PVOUT, measured in kWh/kWp per year. Data is from the Global Solar Atlas, updated in 2020. This will give us insight into potential for the solar developer and agricultural yield, helping determine which crops are most suitable for the area.

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
            if done==1: # add actual logic to downlaod the correct report (when the other reports are written)
                a.report("Grazers-Pollinators")
        except:
            # actually go in and do "except <specific error>" to be more helpful i.e. invalid state, county ...
            st.warning("Invalid inputs! Please try again")
            a.delete()