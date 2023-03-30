import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests, json

# Config Variables
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

"""Return a dictionary of all available locations with ID and Name attributes."""
def get_locations():
        # Monitoring Location
        attribute_ids = requests.get('https://data.chesapeakebay.net/api.json/' + geographical_attribute)
        attribute_data = json.loads(attribute_ids.text)
        attribute_name = geographical_attribute + "Name"
        attribute_id = geographical_attribute + "Id"
        
        locations = []
        for attribute in attribute_data:
            current_location_id = attribute[attribute_id]
            current_location_name = attribute[attribute_name]
            locations.append(dict(id = current_location_id, name = current_location_name))
        return locations

def get_location_names(available_locations):
        available_locations = get_locations()
        location_names = []
        for location in available_locations:
              location_names.append(location['name'])
        return location_names

"""Load the home page."""
def home_page():
        # Initialize Home Window Elements
        root = tk.Tk()

        #Set a logo later
        # root.iconbitmap("favicon.ico")
        
        root.geometry("500x500")
        root.title("Chesapeake Checkup")

        select_location_frame = tk.Frame(root)

        label = tk.Label(root, text="Chesapeake Checkup", font=('Arial', 24))
        label.pack(padx=20, pady=20)

        selected_location = tk.StringVar()
        location_cb = ttk.Combobox(select_location_frame, textvariable=selected_location, state="readonly")
        
        # Populate combobox with locations sorted by name
        available_locations = get_locations()
        location_names = get_location_names(available_locations)
        location_names.sort()
        location_cb['values'] = location_names
        location_cb.set('Select a Watershed')
        location_cb.pack(side=tk.LEFT, padx=5)

        """ Create a function to read the combobox every time it is edited and suggest autofill options as the user types.
            Also set the default value again every time it is blank.
        """

        select_location_btn = tk.Button(select_location_frame, text = 'Select Watershed')
        select_location_btn.pack(side=tk.LEFT, padx=5)

        select_location_frame.pack()
        

        root.mainloop()

if __name__ == "__main__":
    home_page()