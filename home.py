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
selected_location = tk.StringVar()

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

def get_data():
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
    
    location_cb = ttk.Combobox(select_location_frame, textvariable=selected_location, state="readonly", font=BUTTON_FONT)

    # Populate combobox with locations sorted by name
    available_locations = get_locations()
    location_names = get_location_names(available_locations)
    location_names.sort()
    location_cb["values"] = location_names
    location_cb.set("Select a Watershed")
    location_cb.pack(side=tk.LEFT, padx=5)

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
    location = selected_location.get()
    stats_window.geometry("500x600")
    stats_window.title(location)
    # Create a Label in New window
    title = tk.Label(stats_window, text=location, font=TITLE_FONT)
    title.pack(pady=10)
    
    recent_measurements_frame = tk.Frame(stats_window)
    measurements_label = tk.Label(recent_measurements_frame, text="Recent Measurements:", font=LABEL_FONT)

    measurements_label.pack()
    url = 'https://datahub.chesapeakebay.net/api.JSON/' + section + '/' + subsection +'/' + start_date + '/' + end_date + '/' + data_stream_data + '/' + program_id + '/' + project_id + '/' + geographical_attribute +'/' + attribute_id + '/' + substance_ids
    # print(url)
    water_quality = requests.get(url)
    
    water_quality_data = json.loads(water_quality.text)
    
    latest_data = {}
    
    for sample in water_quality_data:
        # current_data = {"Parameter":sample["Parameter"], "MeasureValue":sample["MeasureValue"], "SampleDate":sample["SampleDate"]}
        parameter = sample["Parameter"]
        if parameter not in latest_data.keys():
            latest_data[parameter] = sample
        else:
            if sample["SampleDate"] > latest_data[parameter]["SampleDate"]:
                latest_data[parameter] = sample
    print(latest_data)
        # for data in latest_data:
        #     if (data["Parameter"] == current_data["Parameter"]) and (data["SampleDate"] > current_data["SampleDate"]):
        #         latest_data.append(current_data)
                
        # if (relavent_data["Parameter"] not in latest_data):
        #     latest_data.append(relavent_data)
    # print(water_quality_data)
    # print(latest_data)

    
    
    recent_measurements_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=20)
    
    

def main():
    home_window()


if __name__ == "__main__":
    main()
