# import modules and get license
import pandas as pd
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import streamlit as st

# set env
# path/workspace might be an issue for production ?
arcpy.env.workspace = r"C:\Users\alden.summerville\OneDrive - Arup\AgroPV Tool\GIS\AgroPV"

# app header/title
st.write('''
# Dual Land Use - AgroPV Tool
''')
st.markdown('''
## Welcome! Enter ....instructions and background
''')

# ask user for input
# add some error handling
state_t = st.text_input("State: ")
county_t = st.text_input("County: ")
lon_t = st.text_input("Longitude: ")
lat_t = st.text_input("Latitude: ")
# -91.6, 42 (Linn, Iowa)

def test():
    # test printing df
    cols = ["state", "county", "lon", "lat"]
    vals_test = [state_t, county_t, lon_t, lat_t]

    df_test = pd.DataFrame(index=cols)
    df_test["Values"] = vals_test

    st.write('''
    ## Test df
    ''')
    st.write(df_test)

if st.button("Simple Test!"):
    test()

# set variables for testing
lon = -91.6
lat = 42
state = 'Iowa'
county = 'Linn'

class Analysis:
    def ras(self):
        # create point geometry for lon,lat input
        # try and find better way to do this...
        out_path = r"C:\Users\alden.summerville\OneDrive - Arup\AgroPV Tool\GIS\AgroPV"
        out_name = "xytable"
        arcpy.management.CreateTable(out_path, out_name)
        arcpy.management.AddField(out_name, "lon")
        arcpy.management.AddField(out_name, "lat")
        arcpy.management.DeleteField(out_name, "FIELD1")
        arcpy.management.DeleteField(out_name, "OBJECTID")
        with arcpy.da.InsertCursor(out_name,["lon", "lat"]) as cursor:     
            cursor.insertRow((lon, lat))
        arcpy.MakeXYEventLayer_management(out_name, "lon", "lat", "point_input")

        # raster layers and outputs
        ras_list = ["Slope in Degrees.tif", 
                    "PV Output.tif", 
                    "Richness of Imperiled Spe.tif", 
                    "Species Richness.tif", #freshwater
                    "WorldClim Global Mean Pre.tif",
                    "USA Cropland.tif",
                    "USA NLCD Land Cover.tif",
                    "USA National Commodity Cr.tif"]

        outputs = ["slope_percent",
                    "PV_kWh_per_kWp",
                    "imperiled_species_richness",
                    "imperiled_fwater_richness",
                    "precipitation_mm",
                    "primary_crop",
                    "land_cover",
                    "crop_productivity"]

        #get raster values
        count = 0
        for i in ras_list:
            ExtractValuesToPoints("point_input", i, f"{outputs[count]}", "INTERPOLATE")
            count+=1

        # create df
        cols = ["slope_percent.shp",
                "PV_kWh_per_kWp.shp",
                "imperiled_species_richness.shp",
                "imperiled_fwater_richness.shp",
                "precipitation_mm.shp",
                "primary_crop.shp",
                "land_cover.shp",
                "crop_productivity.shp"]

        vals = []
        self.ras = pd.DataFrame(index=outputs)

        tot_rows = 0
        for item in cols:
            rows = arcpy.SearchCursor(item)
            for row in rows:
                tot_rows+=1
                val = row.getValue("RASTERVALU")
                vals.append(val)

        vals_d = vals[0:tot_rows:int(tot_rows/len(cols))]
        self.ras["Values"] = vals_d

        st.write('''
        ## Raster Values
        ''')
        st.write(self.ras)

    def county(self):
        # county layers and outputs
        county_list = ["AgroPV.gdb/USDA_Census_of_Agriculture_2017___Sales_and_Equipment",
                        "AgroPV.gdb/USDA_Census_of_Agriculture_2017___Cattle_Production", 
                        "AgroPV.gdb/National_Risk_Index_Counties__October_2020_"]

        county_cols = ["USDA_Census_of_Agriculture_2017___Sales_and_Equipment.CROP_SALES_IN_DOLLARS",
                        "USDA_Census_of_Agriculture_2017___Cattle_Production.CATTLE_INCL_CALVES_OPERATIONS_W",
                        "National_Risk_Index_Counties__October_2020_.risk_score"]

        outputs = ["crops_sales",
                    "cattle_production",
                    "NRI_score"]

        # get values
        count = 0
        for i in county_list:
            r = i.replace("AgroPV.gdb/", "")
            where_clause = f"{r}.state_name = '{state}' and {r}.county_name = '{county}'"
            arcpy.management.MakeQueryTable(i, outputs[count], "USE_KEY_FIELDS", "{r}.OBJECTID", county_cols[count], where_clause)
            count+=1

        # add county vals to df
        vals = []
        self.county = pd.DataFrame(index=outputs)

        count = 0
        for item in outputs:
            rows = arcpy.SearchCursor(item)
            for row in rows:
                val = row.getValue(county_cols[count])
                vals.append(val)
            count+=1

        self.county["Values"] = vals

        st.write('''
        ## County Values
        ''')
        st.write(self.county.apply(lambda x: '%.4f' % x, axis=1)) # lambda fxn to remove sci notation

    def total(self):
        # join dfs
        final_vals = pd.concat([self.ras,self.county]).apply(lambda x: '%.4f' % x, axis=1)

        st.write('''
        ## Total Values
        ''')
        st.write(final_vals)
    
    def rec():
        # function to give recommendation...
        pass

    def delete():
        # delete all created features (so can run tool again)
        arcpy.management.Delete("xytable")
        arcpy.management.Delete("point_input")
        arcpy.management.Delete("slope_percent.shp")
        arcpy.management.Delete("PV_kWh_per_kWp.shp")
        arcpy.management.Delete("imperiled_species_richness.shp")
        arcpy.management.Delete("imperiled_fwater_richness.shp")
        arcpy.management.Delete("precipitation_mm.shp")
        arcpy.management.Delete("primary_crop.shp")
        arcpy.management.Delete("land_cover.shp")
        arcpy.management.Delete("crop_productivity.shp")
        arcpy.management.Delete("crops_sales")
        arcpy.management.Delete("cattle_production")
        arcpy.management.Delete("NRI_score")
     

# instantiate class
a = Analysis()

# analyze button
if st.button("Analyze!"):
    a.ras()
    a.county()
    a.total()
    a.rec()
    a.delete()