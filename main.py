import tkinter as tk
from tkinter import ttk

import requests, json, tkintermapview
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from idlelib.tooltip import Hovertip

# Config Variables
section = "WaterQuality"
subsection = "WaterQuality"
start_date = "1-1-2019"
end_date = date.today().strftime('%#m-%#d-%Y')
data_stream_data = "0,1"
program_id = "2,4,6"
project_id = "12,13,15,35,36,2,3,7,33,34,23,24"
geographical_attribute = "HUC8"
substance_ids = "123,31,73,104,105"

# Font Constants:
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
plt.rcParams["font.family"] = FONT

# Global variables:
# Create the root tkinter frame
root = tk.Tk()

home_window_icon = tk.PhotoImage(file="icons/bluecrab.png")

# Location selected from main window combobox
selected_location_name = tk.StringVar()
# Metric selected from stats window combobox
selected_metric = tk.StringVar()
# Temporarily store all the markers that are placed
map_markers = []
#Becomes True when the home window combobox updates
location_selected = False

# Pre-load list of substances from the API
substances = requests.get('https://data.chesapeakebay.net/api.json/Substances')
substance_data = json.loads(substances.text)

def get_locations():
    '''Return a dictionary of all available locations with ID and Name attributes.'''
    # Monitoring Location
    url = 'https://data.chesapeakebay.net/api.JSON/' + section + '/Station/' + geographical_attribute
    attribute_ids = requests.get(url)
    attribute_data = json.loads(attribute_ids.text)
    attribute_name = geographical_attribute + "Description"
    
    # FIND A WAY TO MAKE A CONSTANT FOR THIS IN CASE USER WANTS TO CHANGE THIS LATER IN SETTINGS PAGE 
    attribute_id = 'HUCEightId' # geographical_attribute + "Id"
    
    # Get location ID and name for each location, append it to list
    locations = {}
    for attribute in attribute_data:
        current_location_id = attribute[attribute_id]
        current_location_name = attribute[attribute_name]
        locations[current_location_id] = current_location_name
    return locations

def get_location_names(available_locations):
    '''Get the names of locations from a list of available locations'''
    location_names = list(available_locations.values())
    return location_names

def get_location_id(location_name):
    '''Get the ID of a location by its name'''
    available_locations = get_locations()
    for id, name in available_locations.items():
        if name == location_name:
            return id
    print("Error: Location ID Not Found")
    return(-1)

def get_latest_data(water_quality_data):
    '''Get the most recently uploaded data, return it as a list of dictionaries with paramaters as the keys.'''
    latest_data = {}
    for sample in water_quality_data:
        parameter = sample["Parameter"]
        if parameter not in latest_data.keys():
            latest_data[parameter] = sample
        else:
            if sample["SampleDate"] > latest_data[parameter]["SampleDate"]:
                latest_data[parameter] = sample
    return(latest_data)

def get_substance_description(substance_name):
    '''Get the full description of a substance from its name.'''
    substance_data_frame = pd.DataFrame(substance_data)
    substance_description = substance_data_frame.loc[substance_data_frame['SubstanceIdentificationName'] == substance_name]['SubstanceIdentificationDescription']
    return(substance_description.values[0])

def get_substance_name(substance_description):
    '''Get the substance name abbreviation from its full description'''    
    substance_data_frame = pd.DataFrame(substance_data)
    substance_description = substance_data_frame.loc[substance_data_frame['SubstanceIdentificationDescription'] == substance_description]['SubstanceIdentificationName']
    return(substance_description.values[0])

def update_graph(frame, monthly_averages):
    '''Update stats window plot every time a new metric is chosen.'''
    # Clear out the frame (and any previous plots in it)
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Generate the new graph
    plot_frame = tk.Frame(frame)
    substance_description = selected_metric.get()
    substance_name = get_substance_name(substance_description)
    data = monthly_averages.loc[substance_name, :].tail(12)
    figure = plt.Figure(figsize=(4.5,4), dpi=100) #figure size in inches
    figure_plot = figure.add_subplot(1, 1, 1) # num of rows, num of columns, index position
    figure_plot.set_ylabel(substance_description)
    figure.subplots_adjust(bottom=0.15, left=0.15)
    line_graph = FigureCanvasTkAgg(figure, plot_frame)
    line_graph.get_tk_widget().pack(fill=tk.BOTH)
    data.plot(kind='line', legend=False, ax=figure_plot, color='b', marker='o', fontsize=10, xlabel="X Axis Label")

    figure_plot.set_title(('Monthly Average ' + substance_name + ' Over the Last Year'))

    # Show the plot
    plt.show()
    plot_frame.pack()
    frame.pack(pady=10)
    
def get_location_coords(location_id):
    '''Return all coordinates of a location from its ID (latitude, longitude) as a dataframe.'''
    url = 'https://data.chesapeakebay.net/api.JSON/' + section + '/Station/' + geographical_attribute + '/' + str(location_id)
    all_location_coords = requests.get(url)
    all_location_coords_data = json.loads(all_location_coords.text)
    # Get coordinates from each location
    data_frame = pd.DataFrame(all_location_coords_data)
    coord_pairs = data_frame[['Latitude', 'Longitude']].apply(tuple, axis=1).tolist()
    return coord_pairs

def get_mean_coord(coord_pairs):
    '''Return the average coordinates (Latitude, Longitude) from a set of coordinates.'''
    coords = [0, 0]
    for pair in coord_pairs:
        coords[0] += pair[0]
        coords[1] += pair[1]
    coords[0] /= len(coord_pairs)
    coords[1] /= len(coord_pairs)
    return(coords)

def get_extreme_coords(coord_pairs):
    '''Return the top-left and bottom-right boundaries from a list of coordinates.'''
    lat_min = min(coord[0] for coord in coord_pairs)
    lat_max = max(coord[0] for coord in coord_pairs)
    lon_min = min(coord[1] for coord in coord_pairs)
    lon_max = max(coord[1] for coord in coord_pairs)
    
    top_left = [lat_max, lon_min]
    bottom_right = [lat_min, lon_max]
    
    extremes = [top_left, bottom_right]
    return(extremes)

def update_map(map):
    '''Update a map widget to display a new location.'''
    
    location_name = selected_location_name.get()
    location_id = get_location_id(location_name)
    all_location_coordinates = get_location_coords(location_id)
    central_lat, central_lon = get_mean_coord(all_location_coordinates)
    # top_left, bottom_right = get_extreme_coords(all_location_coordinates)
    # existing_markers = map_markers
    
    map.delete_all_marker()

    for lat, lon in all_location_coordinates:
        map.set_marker(lat, lon)
    # Set Coordinates
    # Mean location of all coordinates
    map.set_position(central_lat, central_lon)

    # map.fit_bounding_box((top_left[0], top_left[1]), (bottom_right[0], bottom_right[1]))
    
    # Set A Zoom Level
    map.set_zoom(10)

def location_selected(map):
    if selected_location_name.get() != "Select a Watershed":
        update_map(map)
        
def view_location_button_pressed():
    if selected_location_name.get() != "Select a Watershed":
        stats_window()
    
def home_window():
    """Load the home page."""
    # Set logo
    root.iconphoto(True, home_window_icon)

    root.geometry("400x500")
    root.title("Chesapeake Checkup")
    root.resizable(False, False)
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

    select_location_btn = tk.Button(select_location_frame, text="View", command=view_location_button_pressed, font=BUTTON_FONT)
    select_location_btn.pack(side=tk.LEFT, padx=5)

    select_location_frame.pack()
    
    # Generate a map
    map_frame = tk.Frame(root)
    map = tkintermapview.TkinterMapView(map_frame, width=300, height=300, corner_radius=0)
    map.set_position(38.685819, -76.406935) # The Chesapeake Bay
    map.set_zoom(7)
    map.pack()
    map_frame.pack(pady=30)
    
    location_cb.bind('<<ComboboxSelected>>', lambda event: location_selected(map))

    root.mainloop()

def stats_window():
    '''Stats window with recent data and graphs over time.'''
    stats_window = tk.Toplevel(root)
    location_name = selected_location_name.get()
    
    stats_window.geometry("500x700")
    stats_window.title(location_name)
    stats_window.resizable(False, False)
    
    # Create a Label in New window
    title_frame = tk.Frame(stats_window)
    
    title = tk.Label(title_frame, text=location_name, font=TITLE_FONT)
    title.pack(pady=10)
    
    title_frame.pack()
    
    location_id = str(get_location_id(location_name))
    
    recent_measurements_label_frame = tk.LabelFrame(stats_window, text="Recent Measurements:", font=LABEL_FONT)
    
    url = 'https://datahub.chesapeakebay.net/api.JSON/' + section + '/' + subsection +'/' + start_date + '/' + end_date + '/' + data_stream_data + '/' + program_id + '/' + project_id + '/' + geographical_attribute +'/' + location_id + '/' + substance_ids

    water_quality = requests.get(url)
    water_quality_data = json.loads(water_quality.text)
    
    metric_names = []
    
    latest_data = get_latest_data(water_quality_data)
    
    substance_labels = []
    tool_tips = []
    
    for key in latest_data:
        # Frame for each substance label
        current_substance_frame = tk.Frame(recent_measurements_label_frame)
        
        substance_desc = get_substance_description(key)
        substance_label_title_content = substance_desc + ':'
        substance_label_content = str(latest_data[key]["MeasureValue"]) + ' ' + str(latest_data[key]["Unit"]) # , '(' + latest_data[key]["SampleDate"] + ')'
        substance_label_title = tk.Label(current_substance_frame, text=substance_label_title_content, font=SUBSTANCE_FONT)
        substance_label = tk.Label(current_substance_frame, text=substance_label_content, font=SUBSTANCE_CONTENT_FONT)
        substance_label_title.pack(side=tk.LEFT)
        substance_label.pack(side=tk.LEFT)
        
        #Create tooltips that show the date that each substance data was last updated 
        date = datetime.strptime(latest_data[key]["SampleDate"],"%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y")
        
        tool_tips.append("Last updated: " + date) 
        substance_labels.append(current_substance_frame)
        #Save this key in a list that we can use for our selection combobox later
        metric_names.append(substance_desc)
        
        current_substance_frame.pack()
    
    # Apply tooltips that appear when user hovers over labels
    for label, tooltip in zip(substance_labels, tool_tips):
        Hovertip(label, tooltip, hover_delay=500)
    
    recent_measurements_label_frame.pack(padx=20, pady=5)
    
    # Create a combobox for selecting the metric that will be graphed.
    select_metric_frame = tk.Frame(stats_window)
    
    select_metric_label = tk.Label(select_metric_frame, text="Select a Metric to Graph Over Time:", font=BUTTON_FONT)
    select_metric_label.pack(side=tk.TOP, anchor=tk.NW)

    metric_cb = ttk.Combobox(select_metric_frame, textvariable=selected_metric, state="readonly", font=BUTTON_FONT)
    metric_names.sort()
    metric_cb["values"] = metric_names

    metric_cb.pack(side=tk.LEFT, padx=10)
    metric_cb.set("Select a Metric")
    
    select_metric_frame.pack(pady=5)
    
    # Store data in a dataframe to be plotted
    data_frame = pd.DataFrame(water_quality_data)
    data_frame = data_frame[["Parameter", "MeasureValue", "Unit", "SampleDate"]]
    data_frame["SampleDate"] = pd.to_datetime(data_frame["SampleDate"], format="%Y-%m-%dT%H:%M:%S")
    monthly_averages = pd.DataFrame(data_frame.groupby(['Parameter', pd.Grouper(key='SampleDate', freq='M')])['MeasureValue'].mean())
    
    plot_frame_wrapper = tk.Frame(stats_window)
    
    # On combobox change, update the graph
    metric_cb.bind('<<ComboboxSelected>>', lambda event: update_graph(plot_frame_wrapper, monthly_averages))

    
def main():
    home_window()

if __name__ == "__main__":
    main()
