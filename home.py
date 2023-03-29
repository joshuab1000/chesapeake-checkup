import tkinter as tk
from tkinter import ttk
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
        return(locations)

def home_page():
        root = tk.Tk()
        root.geometry("500x500")
        root.title("Chesapeake Checkup")

        label = tk.Label(root, text="Chesapeake Checkup", font=('Arial', 24))
        label.pack(padx=20, pady=20)

        selected_location = tk.StringVar()
        location_cb = ttk.Combobox(root, values=selected_location)
        available_locations = get_locations()
        location_names = []
        for location in available_locations:
              location_names.append(location['name'])
        
        location_names.sort()
        location_cb['values'] = location_names
        location_cb.pack()

        root.mainloop()

if __name__ == "__main__":
    home_page()