# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Smoothie Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Smoothie Flavor Survey 📝")
st.write("Please fill out the form below to add your favorite smoothie flavor.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.

st.title("Smoothie Flavor Survey")
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What is your favorite smoothie flavor:")
    value_input = st.text_input("Rate it on a scale of 1-10:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Flavor")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        
        # --- YOUR LOGIC GOES HERE ---
        addRow = [category_input, value_input]
        fileDoesExist = os.path.exists('data.csv')
        with open('data.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not fileDoesExist:
                writer.writerow([category_input, value_input])
            writer.writerow(addRow)
                
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
