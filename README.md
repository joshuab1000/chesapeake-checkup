# Chesapeake Checkup

### About
Chesapeake Checkup is a Windows desktop application written in Python using Tkinter that enables water quality monitoring of the Chesapeake Bay's many watersheds using the [Chesapeake Bay DataHub API](http://datahub.chesapeakebay.net/API).

## Installation

Download all files from the `main` repository, or copy `main.py` and the `icons` directory separately to the same directory.  

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following libraries: [Requests](https://requests.readthedocs.io/en/latest/), [Pandas](https://pandas.pydata.org/), [Matplotlib](https://matplotlib.org/), and [Tkintermapview](https://github.com/TomSchimansky/TkinterMapView).

```bash
pip install matplotlib, requests, pandas, tkintermapview
```

## Usage Instructions

1. Run `main.py`.
2. Use the dropdown menu to select a location that you'd like to view data for.
    - Each time a location is selected, it is shown on the map below.
3. Press the button labelled "View" to open a new window for the selected location.
   
4. On the new location-specific window, there is a frame labeled "Recent Measurements. Hover over any of the listed data with your cursor to show a tooltip that displays exactly what day that data was updated last.
5. Use the dropdown menu beneath the Recent Measurements display to select a metric you'd like to see graphed.
    - Each time a metric is selected, a graph of the monthly average for that metric over the last twelve months at the current location is shown automatically.

## Credits

The logos for this app were created by [Alexander Jenkins](https://github.com/alexander-jenkins) and Ryan Hurst.