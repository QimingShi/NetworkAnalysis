#Import modules
import os
import arcpy
import datetime

#Define variables
workspace = "D:\QimingShi\disease_visualization\Staph\closest_facility.gdb"
output_folder = "D:\QimingShi\disease_visualization\Staph\closest_facility_layer"
nds = "D:\QimingShi\disease_visualization\Staph\Road_Inventory_ND.nd"
inDestinations = os.path.join(workspace, "MA_90")
inOrgins = os.path.join(workspace, "MA_90")
analysis_layer_name = "ClosestFacility"

#Set environment variables
arcpy.env.overwriteOutput = True

#Check out the network analyst extension
arcpy.CheckOutExtension("network")

#Create a new closest facility analysis layer
##make_layer_result = arcpy.na.MakeClosestFacilityLayer(nds, analysis_layer_name,
##                                                      "Length","TRAVEL_TO","",default_number_facilities_to_find=5)

make_layer_result = arcpy.na.MakeODCostMatrixLayer(nds, analysis_layer_name,
                                            "Length", "", "1387","")

analysis_layer = make_layer_result.getOutput(0)

#Add facilities and incidents to the analysis layer using default field mappings         
sub_layer_names = arcpy.na.GetNAClassNames(analysis_layer)
facility_layer_name = sub_layer_names["Origins"]
incident_layer_name = sub_layer_names["Destinations"]

input_feature = "D:\QimingShi\disease_visualization\Staph\closest_facility.gdb\\result29"


##field mapping
fm_type = arcpy.FieldMap()
fm_diam = arcpy.FieldMap()
fms = arcpy.FieldMappings()
fm_type.addInputField(inDestinations, "Name")
fm_diam.addInputField(inDestinations, "Total_Length")
fms.addFieldMap(fm_type)
fms.addFieldMap(fm_diam)

i=0

for row in arcpy.SearchCursor(inOrgins):
    i = i +1
    rows = arcpy.InsertCursor("D:\QimingShi\disease_visualization\Staph\closest_facility.gdb\\result29")
    rows.insertRow(row)
    if (i%50 == 0 and i<=1350) or i ==1387:
        print i
        print rows
        print str(datetime.datetime.now())

        arcpy.na.AddLocations(analysis_layer, facility_layer_name, input_feature, "Name PAT_MRN_ID #", "#",append="CLEAR")
        arcpy.na.AddLocations(analysis_layer, incident_layer_name, inDestinations, "Name PAT_MRN_ID #", "#",append="CLEAR")
        print str(datetime.datetime.now())
#Get the Trucking Time travel mode from the network dataset
        travel_modes = arcpy.na.GetTravelModes(nds)
        trucking_mode = travel_modes

#Apply the travel mode to the analysis layer
        solver_properties = arcpy.na.GetSolverProperties(analysis_layer)
        solver_properties.applyTravelMode()

#Solve the analysis layer and save the result as a layer file          
        arcpy.na.Solve(analysis_layer)
        print str(datetime.datetime.now())
        output_layer = os.path.join(output_folder, analysis_layer_name + str(i) +".lyr")
        text_file_name = os.path.join("text" +str(i)+".txt")
        print str(datetime.datetime.now())
        ODLinesSubLayer = arcpy.mapping.ListLayers(analysis_layer, "lines")[0] 
        arcpy.management.SaveToLayerFile(analysis_layer, output_layer, "RELATIVE")
        arcpy.TableToTable_conversion(ODLinesSubLayer,r"D:\QimingShi\disease_visualization\Staph\text_file",text_file_name,"",fms)
# Delete cursor and row objects to remove locks on the data
        del row
        del rows
        arcpy.DeleteRows_management("D:\QimingShi\disease_visualization\Staph\closest_facility.gdb\\result29")
##arcpy.AddMessage("Completed")
