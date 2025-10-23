# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations for Flavor Ratings 📈")
st.write("This page displays graphs based on the collected data of smoothie flavors.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

st.info("TODO: Add your Flavor Ratings here.")


if "csv_data" not in st.session_state:
    try:        
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data.csv")
        csv_path = os.path.abspath(csv_path)

        if os.path.exists(csv_path):
            st.session_state.csv_data = pd.read_csv(csv_path)
        else:
            st.warning(f"CSV file not found at {csv_path}")
            st.session_state.csv_data = pd.DataFrame()
         
    except:
        st.session_state.csv_data = pd.DataFrame() 
if "json_data" not in st.session_state:
    try:
        json_path = os.path.join(os.path.dirname(__file__), "..", "data.json")

        if os.path.exists(json_path):
            with open(json_path, "r") as file:
                data = json.load(file)                        
            if isinstance(data, list):
                st.session_state.json_data = pd.DataFrame(data)
            elif isinstance(data, dict) and "dataPoints" in data:
                st.session_state.json_data = pd.DataFrame(data["dataPoints"])
            else:
                st.session_state.json_data = pd.DataFrame()
        else:
            st.session_state.json_data = pd.DataFrame()
    except:
        st.session_state.json_data = pd.DataFrame()
st.header("CSV Data")
if not st.session_state.csv_data.empty:
    st.write(st.session_state.csv_data)
else:
    st.write("No CSV data was found.")
st.header("JSON Data")
if not st.session_state.json_data.empty:
    st.write(st.session_state.json_data)
else:
    st.write("JSON is empty.")







# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider() #NEW
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Favorite Smoothie Flavors (Static Bar Chart)")
st.write("Bar chart shows number of people that chose a smoothie flavor as their favorite")
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.

st.subheader("Graph 1: Favorite Smoothie Flavors (Static Bar Chart)")
st.write("Bar chart shows number of people that chose a smoothie flavor as their favorite")

if not st.session_state.csv_data.empty:
    if "Category" in st.session_state.csv_data.columns:
        st.bar_chart(st.session_state.csv_data.set_index("Category"))
    else:
        st.warning(f"Expected 'Category' column not found. Columns found: {st.session_state.csv_data.columns.tolist()}")
else:
    st.warning("CSV data is empty or not loaded.")                        
        

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Flavor Type Ratings (CSV Dynamic)")
# CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Line Chart displays select number of flavors of your choosing with the slider")
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
if "rowNumbers" not in st.session_state: 
    st.session_state.rowNumbers = 2
if not st.session_state.csv_data.empty:
    rowMaximum = len(st.session_state.csv_data)
    st.session_state.rowNumbers = st.slider( #NEW
        "Select number of smoothie flavors to show",
        min_value = 1,
        max_value = rowMaximum,
        value = st.session_state.rowNumbers
    )

    changedData = st.session_state.csv_data.head(st.session_state.rowNumbers)
    st.line_chart(changedData.set_index("Category")) #NEW
else:
    st.warning("No CSV data available to display the line chart.")#NEW


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Smoothie Ratings (Dynamic Pie Chart)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
st.write("Move the slider to filter out smoothies based on a minimum rating.")
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.
# Example: make sure json_data is actually loaded into session state
# (either from a file_uploader or a local file)
# if "json_data" not in st.session_state:
# with open("data.json", "r", encoding="utf-8") as f:
# st.session_state.json_data = json.load(f)




if "minimumRating" not in st.session_state:
    st.session_state.minimumRating = 0
if "json_data" in st.session_state and not st.session_state.json_data.empty:    
    json_df = st.session_state.json_data  #NEW  
    st.session_state.minimumRating = st.slider(
        "Choose a minimum rating",
        0, 10, st.session_state.minimumRating
    )    
    if "value" in json_df.columns and "label" in json_df.columns:
        filtered_json = json_df[json_df["value"] >= st.session_state.minimumRating]        
        if not filtered_json.empty:
            st.area_chart(filtered_json.set_index("label"))#NEW
        else:
            st.write("No smoothies were able to be found with a minimum rating above this value.")
    else:
        st.warning("JSON data is not in the correct columns.")
else:
    st.warning("JSON data is not available.")


