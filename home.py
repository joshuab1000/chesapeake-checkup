import tkinter as tk
from tkinter import ttk

# from PIL import Image, ImageTk # For icon and images later
import requests, json
from datetime import date

# Config Variables
section = "WaterQuality"
subsection = "WaterQuality"

start_date = "2-21-2022"
end_date = date.today().strftime('%#m-%#d-%Y')
data_stream_data = "0,1"
program_id = "2,4,6"
project_id = "12,13,15,35,36,2,3,7,33,34,23,24"
geographical_attribute = "HUC8"
attribute_id = "26"
substance_ids = "123,31,73,104,105"

# Font Constants
FONT = "Calibri"
TITLE_SIZE = 24
TITLE_FONT = (FONT, TITLE_SIZE)
BUTTON_SIZE = 10
BUTTON_FONT = (FONT, BUTTON_SIZE)
LABLE_SIZE = 16
LABEL_FONT = (FONT, LABLE_SIZE)

root = tk.Tk()
# Location selected from main window combobox
selected_location_name = tk.StringVar()
# available_locations = []

def get_locations():
    """Return a dictionary of all available locations with ID and Name attributes."""
    # Monitoring Location
    attribute_ids = requests.get("https://data.chesapeakebay.net/api.json/" + geographical_attribute)
    attribute_data = json.loads(attribute_ids.text)
    attribute_name = geographical_attribute + "Name"
    attribute_id = geographical_attribute + "Id"
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

def get_parameter_info(parameter):
    """Get name and definition of each parameter"""
    pass

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
    
    stats_window.geometry("500x600")
    stats_window.title(location_name)
    # Create a Label in New window
    title = tk.Label(stats_window, text=location_name, font=TITLE_FONT)
    title.pack(pady=10)
    
    location_id = str(get_location_id(location_name))
    
    recent_measurements_frame = tk.Frame(stats_window)
    measurements_label = tk.Label(recent_measurements_frame, text="Recent Measurements:", font=LABEL_FONT)

    measurements_label.pack()
    
    url = 'https://datahub.chesapeakebay.net/api.JSON/' + section + '/' + subsection +'/' + start_date + '/' + end_date + '/' + data_stream_data + '/' + program_id + '/' + project_id + '/' + geographical_attribute +'/' + location_id + '/' + substance_ids

    water_quality = requests.get(url)
    water_quality_data = json.loads(water_quality.text)
    
    latest_data = get_latest_data(water_quality_data)
    
    for key in latest_data:
        print(key + ':', latest_data[key]["MeasureValue"], latest_data[key]["Unit"], '(' + latest_data[key]["SampleDate"] + ')')
        
    """
    Create a loop that adds these as elements instead of printing them in the console.
    Then, write a function that gets the full name and description of each parameter.
    """
    
    recent_measurements_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=20)
    
    

def main():
    home_window()


if __name__ == "__main__":
    main()
