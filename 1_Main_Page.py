# 1_Main_Page.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import openai
import os

# Load datasets
data = pd.read_csv('Pages/DAta/Synthetic Water Usage.csv')
lower_data = pd.read_csv('Pages/DAta/Lower Synthetic Water Usage.csv')

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Main page setup with water-themed styling
st.markdown("""
    <style>
        .main-title {
            font-size: 2em;
            color: #1E88E5;
            font-weight: bold;
            text-align: center;
            padding: 0.5em;
        }
        .section-title {
            color: #0277BD;
            font-weight: bold;
            font-size: 1.5em;
            padding-top: 1em;
        }
        .sidebar .sidebar-content {
            background-color: #E3F2FD;
            padding: 1em;
        }
        .stButton>button {
            background-color: #29B6F6;
            color: #FFFFFF;
            font-weight: bold;
            border-radius: 10px;
            padding: 0.5em 1em;
        }
        .stButton>button:hover {
            background-color: #0288D1;
            color: #E3F2FD;
        }
        .stAlert {
            background-color: #81D4FA;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">💧 Water Usage Tracker</h1>', unsafe_allow_html=True)
st.sidebar.markdown("# Main Page 🎈")

# Intro message
st.write("This application helps you track and optimize your household water usage with personalized insights. 🌊")

# User Input Section
st.markdown('<div class="section-title">Enter Household Details</div>', unsafe_allow_html=True)
household_size = st.number_input("Number of people in household", min_value=1, step=1)
state = st.selectbox("City", [
    "Gilroy", "San Martin", "Morgan Hill", "Los Gatos", "Monte Sereno", 
    "Campbell", "Saratoga", "San Jose", "Milpitas", "Santa Clara", 
    "Sunnyvale", "Cupertino", "Los Altos", "Mountain View", "Palo Alto", 
    "L.A. Hills"
])

# Prompt Tone Selection
st.markdown('<div class="section-title">Choose Advice Style</div>', unsafe_allow_html=True)
advice_style = st.radio("Select the style of advice you would like to receive:", ("Concise tips", "Detailed advice", "Friendly reminders"))

# Input Desired Savings Goal
savings_goal = st.number_input("Enter your target savings on the water bill (USD)", min_value=0.0, step=1.0)

# Process Data and Display Report
if st.button("Generate Report"):
    st.markdown('<div class="section-title">Daily Water Usage Report</div>', unsafe_allow_html=True)
    
    # Ensure only numeric columns are used for averaging
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    avg_usage = data[numeric_columns].mean().to_dict()
    
    # Display the average daily water usage for each activity
    avg_usage_df = pd.DataFrame(list(avg_usage.items()), columns=["Activity", "Average Daily Gallons"])
    st.write("Here is your average daily water usage for each activity:")
    st.table(avg_usage_df)

    # Calculate Financial Estimates
    st.markdown('<div class="section-title">Estimated Water Costs</div>', unsafe_allow_html=True)
    cost_per_gallon = 0.004  # Cost per gallon in USD
    total_usage = avg_usage_df["Average Daily Gallons"].sum()
    estimated_cost_daily = total_usage * cost_per_gallon
    estimated_cost_monthly = estimated_cost_daily * 30
    estimated_cost_yearly = estimated_cost_daily * 365

    st.write(f"**Estimated Daily Cost**: ${estimated_cost_daily:.2f}")
    st.write(f"**Estimated Monthly Cost**: ${estimated_cost_monthly:.2f}")
    st.write(f"**Estimated Yearly Cost**: ${estimated_cost_yearly:.2f}")

    # Water Usage Trend Forecast with both datasets
    st.markdown('<div class="section-title">Water Usage Trend Over Time</div>', unsafe_allow_html=True)

    # Prepare data from both datasets for plotting
    data['Date'] = pd.to_datetime(data['Date'])
    lower_data['Date'] = pd.to_datetime(lower_data['Date'])

    data.set_index('Date', inplace=True)
    lower_data.set_index('Date', inplace=True)

    trend_data_combined = pd.DataFrame({
        'Your Usage (gallons)': data['Total Usage (gallons)'],
        'State Average (gallons)': lower_data['Total Usage (gallons)']
    })

    # Display the combined line chart with themed colors
    st.line_chart(trend_data_combined, height=300, use_container_width=True)

    # Store variables for use in the Insights page
    st.session_state["data"] = data
    st.session_state["household_size"] = household_size
    st.session_state["state"] = state
    st.session_state["total_usage"] = total_usage
    st.session_state["savings_goal"] = savings_goal
    st.session_state["advice_style"] = advice_style
else:
    st.warning("Please fill out all fields to generate the report.")
