from arcpy.ia.Functions import FindArgumentStatistics
import pandas as pd
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
import streamlit as st
from streamlit.elements.map import _DEFAULT_COLOR
import webbrowser
import os

class Analysis:

    def input(self):
        # ask user for input
        # add some error handling
        self.state = st.text_input("State: ")
        self.county = st.text_input("County: ")
        st.write('''
        Get lon, lat coordinates from an address [here](https://www.latlong.net/)
        ''')
        self.lat = st.text_input("Latitude: ")
        self.lon = st.text_input("Longitude: ")

        # variables for testing
        # lat = 39.147316
        # lon = -75.57281
        # state = 'Delaware'
        # county = 'Kent'

    def ras(self):
        st.write("Analyzing raster layers...")
        # create point geometry for lon,lat input
        os.chdir("..")
        os.chdir("..")
        os.chdir("..")
        os.chdir("GIS")
        out_path = f"{os.getcwd()}\AgroPV"
        os.chdir("..")
        os.chdir("Python")
        os.chdir("duo-tool")
        os.chdir("app")
        out_name = "xytable"
        arcpy.management.CreateTable(out_path, out_name)
        arcpy.management.AddField(out_name, "lon")
        arcpy.management.AddField(out_name, "lat")
        arcpy.management.DeleteField(out_name, "FIELD1")
        arcpy.management.DeleteField(out_name, "OBJECTID")
        with arcpy.da.InsertCursor(out_name,["lon", "lat"]) as cursor:     
            cursor.insertRow((self.lon, self.lat))
        arcpy.MakeXYEventLayer_management(out_name, "lon", "lat", "point_input")

        # raster layers and outputs
        ras_list = ["Slope in Degrees.tif", 
                    "PV Output.tif", 
                    "Richness of Imperiled Spe.tif",
                    "WorldClim Global Mean Pre.tif",
                    "USA Cropland.tif",
                    "USA NLCD Land Cover.tif",
                    "USA National Commodity Cr.tif"]

        outputs = ["slope_percent",
                    "PV_kWh_per_kWp",
                    "imperiled_species_richness",
                    "precipitation_mm",
                    "primary_crop",
                    "land_cover",
                    "crop_productivity"]

        #get raster values
        count = 0
        for i in ras_list:
            ExtractValuesToPoints("point_input", i, f"{outputs[count]}")
            count+=1

        # create df
        cols = ["slope_percent.shp",
                "PV_kWh_per_kWp.shp",
                "imperiled_species_richness.shp",
                "precipitation_mm.shp",
                "primary_crop.shp",
                "land_cover.shp",
                "crop_productivity.shp"]
        
        df_col_names = ["Terrain Slope (%)",
                        "PV Output (kWh/kWp)",
                        "Richness of Imperiled Species",
                        "Annual Average Precipitation (mm)",
                        "Primary Crop Produced",
                        "Land Use Type",
                        "USA National Commodity Crop Productivity Index"
                        ]

        vals = []
        self.ras = pd.DataFrame(index=df_col_names)

        tot_rows = 0
        for item in cols:
            rows = arcpy.SearchCursor(item)
            for row in rows:
                tot_rows+=1
                val = row.getValue("RASTERVALU")
                vals.append(val)

        # vals_d = vals[0:tot_rows:int(tot_rows/len(cols))]  #this shouldn't be needed
        self.ras["Values"] = vals

        # fix values:
        # replace numeric values with non-numeric where needed (crop type, land use)
        # crop type:
        crop_types = pd.read_csv("data/crop_vals.csv")
        self.ras["Values"]["Primary Crop Produced"] = crop_types["Crop"][self.ras["Values"]["Primary Crop Produced"]]
        # land type:
        land_types = pd.read_csv("data/land_use_types.csv")
        self.ras["Values"]["Land Use Type"] = land_types.loc[land_types["RasterValue"]==self.ras["Values"]["Land Use Type"], "Type"].iloc[0]
        # divide crop index by 1000
        self.ras["Values"]["USA National Commodity Crop Productivity Index"] = self.ras["Values"]["USA National Commodity Crop Productivity Index"]/1000

        st.write("Raster layers complete!")

    def county_analysis(self):
        st.write("Analyzing county layers...")
        # county layers and outputs
        county_list = ["AgroPV.gdb/Average_Number_of_Sheep_and_Lambs_per_100_Acres_of_All_Land_in_Farms___2012",
                        "AgroPV.gdb/USDA_Census_of_Agriculture_2017___Sales_and_Equipment",
                        "AgroPV.gdb/USDA_Census_of_Agriculture_2017___Cattle_Production", 
                        "AgroPV.gdb/National_Risk_Index_Counties__October_2020_"]

        county_cols = ["Average_Number_of_Sheep_and_Lambs_per_100_Acres_of_All_Land_in_Farms___2012.y12_M292_valueText", 
                        "USDA_Census_of_Agriculture_2017___Sales_and_Equipment.CROP_SALES_IN_DOLLARS",
                        "USDA_Census_of_Agriculture_2017___Cattle_Production.CATTLE_INCL_CALVES_OPERATIONS_W",
                        "National_Risk_Index_Counties__October_2020_.risk_score"]

        outputs = ["sheep_lamb_avg",
                    "crops_sales",
                    "cattle_production",
                    "NRI_score"]
        
        df_col_names = ["Average # of Sheep and Lambs per 100 Acres",
                        "USDA Crop Sales",
                        "USDA Cattle Production (# operations with sales)",
                        "National Risk Index (NRI) Score"]

        # get values
        count = 0
        for i in county_list:
            r = i.replace("AgroPV.gdb/", "")
            where_clause = f"{r}.state_name = '{self.state}' and {r}.county_name = '{self.county}'"
            arcpy.management.MakeQueryTable(i, outputs[count], "USE_KEY_FIELDS", "{r}.OBJECTID", county_cols[count], where_clause)
            count+=1

        # add county vals to df
        vals = []
        self.countydf = pd.DataFrame(index=df_col_names)

        count = 0
        for item in outputs:
            rows = arcpy.SearchCursor(item)
            for row in rows:
                val = float(row.getValue(county_cols[count]))
                vals.append(val)
            count+=1

        self.countydf["Values"] = vals
        self.countydf["Values"] = self.countydf["Values"].apply(lambda x: '%.4f' % x) # lambda fxn to remove sci notation
        
        st.write("County layers complete!")

    def total(self):
        # join dfs
        self.final_vals = pd.concat([self.ras,self.countydf])

        st.write('''
        ## Final Values:
        ''')
        st.write(self.final_vals)

    def delete(self):
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
        arcpy.management.Delete("sheep_lamb_avg")
        arcpy.management.Delete("crops_sales")
        arcpy.management.Delete("cattle_production")
        arcpy.management.Delete("NRI_score")

    def report(self, filename):
        st.write('''
        ## Suggested Dual Use Strategy
        ''')
        path = f'{os.getcwd()}\\reports\\{filename}.pdf'
        # if st.button("Download Report"):
        st.write("Downloading Report...")
        webbrowser.open_new(path)