# 1_Main_Page.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import openai
import os
import requests
import json

# Load the primary dataset
data = pd.read_csv('Pages/DAta/Synthetic Water Usage.csv')

# Load the secondary (lower values) dataset
lower_data = pd.read_csv('Pages/DAta/Lower Synthetic Water Usage.csv')

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def get_completion(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a resourceful water saving advisor providing water-saving advice."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Main page setup
st.markdown("# Water Usage Tracker 💧")
st.sidebar.markdown("# Main page 🎈")

# Intro message
st.write("This page provides a water tracking template to help you understand and manage your household water usage. Input your household details and goals to get started!")

# User Input Section
st.subheader("Enter Household Details")
household_size = st.number_input("Number of people in household", min_value=1, step=1)
state = st.selectbox("State", ["CA", "NY", "TX", "FL", "Other"])

# Prompt Tone Selection
st.subheader("Choose Advice Style")
advice_style = st.radio("Select the style of advice you would like to receive:", ("Concise tips", "Detailed advice", "Friendly reminders"))

# Input Desired Savings Goal
savings_goal = st.number_input("Enter your target savings on the water bill (USD)", min_value=0.0, step=1.0)

# Process Data and Display Report
if st.button("Generate Report"):
    st.subheader("Daily Water Usage Report")
    
    # Ensure only numeric columns are used for averaging
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    avg_usage = data[numeric_columns].mean().to_dict()
    
    # Display the average daily water usage for each activity
    avg_usage_df = pd.DataFrame(list(avg_usage.items()), columns=["Activity", "Average Daily Gallons"])
    st.write("Here is your average daily water usage for each activity:")
    st.table(avg_usage_df)

    # Calculate Financial Estimates
    st.subheader("Estimated Water Costs")
    cost_per_gallon = 0.004  # Cost per gallon in USD
    total_usage = avg_usage_df["Average Daily Gallons"].sum()
    estimated_cost_daily = total_usage * cost_per_gallon
    estimated_cost_monthly = estimated_cost_daily * 30
    estimated_cost_yearly = estimated_cost_daily * 365

    st.write(f"**Estimated Daily Cost**: ${estimated_cost_daily:.2f}")
    st.write(f"**Estimated Monthly Cost**: ${estimated_cost_monthly:.2f}")
    st.write(f"**Estimated Yearly Cost**: ${estimated_cost_yearly:.2f}")

    # Water Usage Trend Forecast with both datasets
    st.subheader("Water Usage Trend Over Time")

    # Prepare data from both datasets for plotting
    data['Date'] = pd.to_datetime(data['Date'])
    lower_data['Date'] = pd.to_datetime(lower_data['Date'])

    data.set_index('Date', inplace=True)
    lower_data.set_index('Date', inplace=True)

    trend_data_combined = pd.DataFrame({
        'Users Usage (gallons)': data['Total Usage (gallons)'],
        'Average Statewide Usage (gallons)': lower_data['Total Usage (gallons)']
    })

    # Display the combined line chart
    st.line_chart(trend_data_combined)

    # Store variables for use in the Insights page
    st.session_state["data"] = data
    st.session_state["household_size"] = household_size
    st.session_state["state"] = state
    st.session_state["total_usage"] = total_usage
    st.session_state["savings_goal"] = savings_goal
    st.session_state["advice_style"] = advice_style
else:
    st.warning("Please fill out all fields to generate the report.")



