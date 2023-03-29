import requests, json

section = "WaterQuality"
subsection = "WaterQuality"

start_date = "2-21-2022"
end_date = "2-21-2023"
data_stream_data = "0,1" 
program_id = "2,4,6"
project_id = "12,13,15,35,36,2,3,7,33,34,23,24"
geographical_attribute = "HUC8"
attribute_id = "26"
substance_id = "31"

# Monitoring Location
attribute_ids = requests.get('https://data.chesapeakebay.net/api.json/' + geographical_attribute)
attribute_data = json.loads(attribute_ids.text)
attribute_name = geographical_attribute + "Name"
attribute_id = geographical_attribute + "Id"

# Substances in the Water with Available Data
substance_ids = requests.get('https://data.chesapeakebay.net/api.json/Substances')
substance_data = json.loads(substance_ids.text)

# Water Quality Data for the Selected Location and Substance
water_quality = requests.get('https://datahub.chesapeakebay.net/api.JSON/' + section + '/' + subsection +'/' + start_date + '/' + end_date + '/' + data_stream_data + '/' + program_id + '/' + project_id + '/' + geographical_attribute +'/' + attribute_id + '/' + substance_id)
water_quality_data = json.loads(water_quality.text)

# Console-based Version of App
print("Chesapeake Checkup")

print("Available Bodies of Water:")
locations = []
for attribute in attribute_data:
    current_location = attribute[attribute_name]
    current_location_id = attribute[attribute_id]
    locations.append((current_location, current_location_id))
    print(current_location)
location = " "
print(locations[:][1])
while location not in locations[:][1]:
    location = input("Enter The Name of a Body of Water: ")
location_id = locations[location]
print(attribute_data[int(attribute_id) - 1][attribute_name], substance_data[int(substance_id) - 1]['SubstanceIdentificationName'], water_quality_data[0]['MeasureValue'], water_quality_data[0]['Unit'])

#for substance in substance_data:
    
print(attribute_data[int(attribute_id) - 1][attribute_name], substance_data[int(substance_id) - 1]['SubstanceIdentificationName'], water_quality_data[0]['MeasureValue'], water_quality_data[0]['Unit'])