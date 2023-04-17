import tkinter as tk
from tkinter import ttk

# from PIL import Image, ImageTk # For icon and images later
import requests, json
from datetime import date

# Config Variables
section = "WaterQuality"
subsection = "WaterQuality"

start_date = "1-1-2019"
end_date = date.today().strftime('%#m-%#d-%Y')
data_stream_data = "0,1"
program_id = "2,4,6"
project_id = "12,13,15,35,36,2,3,7,33,34,23,24"
geographical_attribute = "HUC8"
# attribute_id = "26"
substance_ids = "123,31,73,104,105"

# Font Constants
FONT = "Calibri"
TITLE_SIZE = 24
TITLE_FONT = (FONT, TITLE_SIZE)
BUTTON_SIZE = 10
BUTTON_FONT = (FONT, BUTTON_SIZE)
LABLE_SIZE = 16
LABEL_FONT = (FONT, LABLE_SIZE)
SUBSTANCE_FONT_SIZE = 12
SUBSTANCE_FONT = (FONT, SUBSTANCE_FONT_SIZE, 'bold') 
SUBSTANCE_CONTENT_FONT = (FONT, SUBSTANCE_FONT_SIZE)


root = tk.Tk()
# Location selected from main window combobox
selected_location_name = tk.StringVar()
# available_locations = []

def get_locations():
    """Return a dictionary of all available locations with ID and Name attributes."""
    # Monitoring Location
    attribute_ids = requests.get('https://data.chesapeakebay.net/api.JSON/WaterQuality/Station/HUC8/') #"https://data.chesapeakebay.net/api.json/" + geographical_attribute)
    attribute_data = json.loads(attribute_ids.text)
    attribute_name = geographical_attribute + "Description"
    
    # FIND A WAY TO MAKE A CONSTANT FOR THIS IN CASE USER WANTS TO CHANGE THIS LATER IN SETTINGS PAGE 
    attribute_id = 'HUCEightId' # geographical_attribute + "Id"
    
    # Get location ID and name for each location, append it to list
    locations = []
    for attribute in attribute_data:
        current_location_id = attribute[attribute_id]
        current_location_name = attribute[attribute_name]
        
        locations.append(dict(id=current_location_id, name=current_location_name))
    return locations


def get_location_names(available_locations):
    """Get the names of locations from a list of available locations"""
    available_locations = get_locations()
    location_names = []
    for location in available_locations:
        location_names.append(location["name"])
    return location_names

def get_location_id(location_name):
    """Get the ID of a location by its name"""
    available_locations = get_locations()
    for location in available_locations:
        if location["name"] == location_name:
            return location["id"]

def get_latest_data(water_quality_data):
    """Get the most recently uploaded data, return it as a list of dictionaries with paramaters as the keys"""
    latest_data = {}
    
    for sample in water_quality_data:
        # current_data = {"Parameter":sample["Parameter"], "MeasureValue":sample["MeasureValue"], "SampleDate":sample["SampleDate"]}
        parameter = sample["Parameter"]
        if parameter not in latest_data.keys():
            latest_data[parameter] = sample
        else:
            if sample["SampleDate"] > latest_data[parameter]["SampleDate"]:
                latest_data[parameter] = sample
    return(latest_data)

def get_substance_description(substance_name):
    """Get the full description of a substance from its name"""
    
    substances = requests.get('https://data.chesapeakebay.net/api.json/Substances')
    substance_data = json.loads(substances.text)
    
    for substance in substance_data:
            if substance["SubstanceIdentificationName"] == substance_name:
                # print(substance["SubstanceIdentificationDescription"])
                return(substance["SubstanceIdentificationDescription"])
    
    print("SUBSTANCE" + substance_name + "NOT FOUND:")
    return "error"

def home_window():
    """Load the home page."""
    
    # Initialize Home Window Elements

    # Set a logo later
    # root.iconbitmap("favicon.ico")

    root.geometry("500x250")
    root.title("Chesapeake Checkup")
    select_location_frame = tk.Frame(root)

    label = tk.Label(root, text="Chesapeake Checkup", font=TITLE_FONT)
    label.pack(padx=20, pady=20)
    
    select_label = tk.Label(select_location_frame, text="Select a Watershed:", font=BUTTON_FONT)
    select_label.pack(side=tk.TOP, anchor=tk.NW)
    
    location_cb = ttk.Combobox(select_location_frame, textvariable=selected_location_name, state="readonly", font=BUTTON_FONT)

    # Populate combobox with locations sorted by name
    available_locations = get_locations()
    location_names = get_location_names(available_locations)
    location_names.sort()
    location_cb["values"] = location_names
    location_cb.set("Select a Watershed")
    location_cb.pack(side=tk.LEFT, padx=5)

    # print(available_locations[selected_location_name]["id"])

    # available_locations[selected_location_name]

    """
        Create a function to read the combobox every time it is edited and suggest autofill options as the user types.
        Also set the default value again every time it is blank.
    """

    select_location_btn = tk.Button(select_location_frame, text="View", command=stats_window, font=BUTTON_FONT)
    select_location_btn.pack(side=tk.LEFT, padx=5)

    select_location_frame.pack()

    root.mainloop()

def stats_window():
    stats_window = tk.Toplevel(root)
    location_name = selected_location_name.get()
    
    stats_window.geometry("450x600")
    stats_window.title(location_name)
    # Create a Label in New window
    title = tk.Label(stats_window, text=location_name, font=TITLE_FONT)
    title.pack(pady=10)
    
    location_id = str(get_location_id(location_name))
    
    recent_measurements_label_frame = tk.LabelFrame(stats_window, text="Recent Measurements:", font=LABEL_FONT)
    # measurements_label = tk.Label(recent_measurements_label_frame, text="Recent Measurements:", font=LABEL_FONT)
    # measurements_label.pack(side=tk.LEFT)
    # substance_label_frame = tk.LabelFrame(stats_window, text="Recent Measurements")
    
    url = 'https://datahub.chesapeakebay.net/api.JSON/' + section + '/' + subsection +'/' + start_date + '/' + end_date + '/' + data_stream_data + '/' + program_id + '/' + project_id + '/' + geographical_attribute +'/' + location_id + '/' + substance_ids

    water_quality = requests.get(url)
    water_quality_data = json.loads(water_quality.text)
    
    latest_data = get_latest_data(water_quality_data)
    print(location_name + ":")
    for key in latest_data:
        current_substance_frame = tk.Frame(recent_measurements_label_frame)
        
        substance_desc = get_substance_description(key)
        substance_label_title_content = substance_desc + ':'
        substance_label_content = str(latest_data[key]["MeasureValue"]) + ' ' + str(latest_data[key]["Unit"]) # , '(' + latest_data[key]["SampleDate"] + ')'
        # print(substance_label_content)
        substance_label_title = tk.Label(current_substance_frame, text=substance_label_title_content, font=SUBSTANCE_FONT)
        substance_label = tk.Label(current_substance_frame, text=substance_label_content, font=SUBSTANCE_CONTENT_FONT)
        substance_label_title.pack(side=tk.LEFT)
        substance_label.pack(side=tk.LEFT)
        
        current_substance_frame.pack()
    # substance_label_frame.pack()
    
    recent_measurements_label_frame.pack(padx=20)


    """
    Create a loop that adds these as elements instead of printing them in the console.
    Then, write a function that gets the full name and description of each parameter.
    """


def main():
    home_window()


if __name__ == "__main__":
    main()
