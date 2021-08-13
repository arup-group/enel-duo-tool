# Enel Dual Use Opportunities Tool (DUO)

## This tool is intended as a resource to assist with planning and implementing dual use solar options so to achieve better outcomes

The tool consists of a python script with ArcGIS functionality (arcpy package) in order to calculate the values for various map layers, then provide a recommendation based on the site conditions.

## Development

Open the [duo-tool](https://arup.sharepoint.com/:f:/s/EnelCircularEconomy/Eh_5fsO6wHZFrAKn5AWlS9MBetDYvZ6wT-cYb1rsncJptA?e=690SLe) Arup One Drive folder in an IDE of your choice. This is necessary as the ArcGIS Pro workspace has to be relative to the project code in order for the code to read from the workspace -- this doesn't mean ArcGIS Pro has to be running for the app to run, the GIS workspace simply needs to exist. Therefore, one cannot simply clone this repo to successfully utilize the app functionality

## Dependencies

### conda

**ArcPy**: The primary python module requirement for this project is the [Arcpy](https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/installing-arcpy.htm) module from ESRI. Create an Anaconda environment for your development  `conda create --name <env name>`, then `conda install -c esri arcpy` to install the module. If this fails, you probably don't have ArcGIS Pro on your machine (using a remote workstation is an easy fix). The "Spatial Analyst" toolbox in ArcGIS is necessary for the functionality of the app, so make sure that license is turned on in ArcGIS Pro (Project, Licensing, Configure your Licensing Options, then make sure "Spatial Analyst" is selected)

### pip

**streamlit**

**pandas**

## Running the App

To run the web-app with Streamlit, cd to the app directory and run `streamlit run login.py`
