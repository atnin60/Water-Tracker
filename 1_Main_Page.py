# 1_Main_Page.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import openai
import os
import matplotlib.pyplot as plt

# Load datasets
data = pd.read_csv('Pages/DAta/Synthetic Water Usage.csv')
city_files = {
    "L.A. Hills": "Pages/DAta/L.A._Hills_Water_Usage.csv",
    "Palo Alto": "Pages/DAta/Palo_Alto_Water_Usage.csv",
    "Mountain View": "Pages/DAta/Mountain_View_Water_Usage.csv",
    "Los Altos": "Pages/DAta/Los_Altos_Water_Usage.csv",
    "Santa Clara": "Pages/DAta/Santa_Clara_Water_Usage.csv",
    "San Jose": "Pages/DAta/San_Jose_Water_Usage.csv",
    "Monte Sereno": "Pages/DAta/Monte_Sereno_Water_Usage.csv",
    "Los Gatos": "Pages/DAta/Los_Gatos_Water_Usage.csv",
    "Morgan Hill": "Pages/DAta/Morgan_Hill_Water_Usage.csv",
}

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
city = st.selectbox("Choose a city:", list(city_files.keys()))

# Prompt Tone Selection
st.markdown('<div class="section-title">Choose Advice Style</div>', unsafe_allow_html=True)
advice_style = st.radio("Select the style of advice you would like to receive:", ("Concise tips", "Detailed advice", "Friendly reminders"))

# Input Desired Savings Goal
savings_goal = st.number_input("Enter your target savings on the water bill (USD)", min_value=0.0, step=1.0)

# Process Data and Display Report
if st.button("Generate Report"):
    st.markdown('<div class="section-title">Daily Water Usage Report</div>', unsafe_allow_html=True)

    # Fetch the file path for the selected city
    data_path = city_files[city]

    # Load the corresponding CSV data
    lower_data = pd.read_csv(data_path)
    
    # Ensure only numeric columns are used for averaging
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    avg_usage = data[numeric_columns].mean().to_dict()
    
    # Remove 'Total Usage (gallons)' from the bar graph
    avg_usage.pop("Total Usage (gallons)", None)
    
    # Display the average daily water usage for each activity as a table
    avg_usage_df = pd.DataFrame(list(avg_usage.items()), columns=["Activity", "Average Daily Gallons"])
    st.write("Here is your average daily water usage for each activity:")
    st.table(avg_usage_df)

    # Create and display the bar graph for daily water usage
    st.markdown('<div class="section-title">Visualizing Your Daily Water Usage</div>', unsafe_allow_html=True)
    fig_bar, ax_bar = plt.subplots()
    ax_bar.bar(avg_usage_df["Activity"], avg_usage_df["Average Daily Gallons"], color='#29B6F6')
    ax_bar.set_title("Average Daily Water Usage by Activity", fontsize=16, color='#0277BD')
    ax_bar.set_ylabel("Gallons", fontsize=14, color='#0277BD')
    ax_bar.set_xlabel("Activity", fontsize=14, color='#0277BD')
    ax_bar.tick_params(axis='x', rotation=45)
    st.pyplot(fig_bar)

    # Calculate Financial Estimates
    st.markdown('<div class="section-title">Estimated Water Costs</div>', unsafe_allow_html=True)
    cost_per_gallon = 0.1  # Cost per gallon in USD
    total_usage = avg_usage_df["Average Daily Gallons"].sum()
    estimated_cost_daily = total_usage * cost_per_gallon
    estimated_cost_monthly = estimated_cost_daily * 30
    estimated_cost_yearly = estimated_cost_daily * 365

    total_usage_city = lower_data["Total Usage (gallons)"].sum()
    estimated_cost_daily_city = total_usage_city * cost_per_gallon
    estimated_cost_monthly_city = estimated_cost_daily_city * 30
    estimated_cost_yearly_city = estimated_cost_daily_city * 365

    st.write("**Preset Database (State Average) Costs**")
    st.write(f"**Estimated Daily Cost**: ${estimated_cost_daily:.2f}")
    st.write(f"**Estimated Monthly Cost**: ${estimated_cost_monthly:.2f}")
    st.write(f"**Estimated Yearly Cost**: ${estimated_cost_yearly:.2f}")

    st.write("**Selected City Costs**")
    st.write(f"**Estimated Daily Cost**: ${estimated_cost_daily_city:.2f}")
    st.write(f"**Estimated Monthly Cost**: ${estimated_cost_monthly_city:.2f}")
    st.write(f"**Estimated Yearly Cost**: ${estimated_cost_yearly_city:.2f}")

    # Water Usage Trend Forecast with both datasets
    st.markdown('<div class="section-title">Water Usage Trend Over Time</div>', unsafe_allow_html=True)

    # Prepare data from both datasets for plotting
    data['Date'] = pd.to_datetime(data['Date'])
    lower_data['Date'] = pd.to_datetime(lower_data['Date'])

    data.set_index('Date', inplace=True)
    lower_data.set_index('Date', inplace=True)

    trend_data_combined = pd.DataFrame({
        'Your Usage (gallons)': data['Total Usage (gallons)'],
        'City Average (gallons)': lower_data['Total Usage (gallons)']
    })

    # Create and display the trend line chart with custom Matplotlib
    fig_trend, ax_trend = plt.subplots(figsize=(10, 6))
    ax_trend.plot(trend_data_combined.index, trend_data_combined['Your Usage (gallons)'], label='Your Usage (gallons)', color='blue', linewidth=2)
    ax_trend.plot(trend_data_combined.index, trend_data_combined['City Average (gallons)'], label='City Average (gallons)', color='orange', linewidth=2)
    ax_trend.set_title("Water Usage Trend Over Time", fontsize=16, color='#0277BD')
    ax_trend.set_xlabel("Date", fontsize=14, color='#0277BD')
    ax_trend.set_ylabel("Gallons", fontsize=14, color='#0277BD')
    ax_trend.legend(fontsize=12)
    ax_trend.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    st.pyplot(fig_trend)

    # Store variables for use in the Insights page
    st.session_state["data"] = data
    st.session_state["household_size"] = household_size
    st.session_state["city"] = city
    st.session_state["total_usage"] = total_usage
    st.session_state["savings_goal"] = savings_goal
    st.session_state["advice_style"] = advice_style
else:
    st.warning("Please fill out all fields to generate the report.")
