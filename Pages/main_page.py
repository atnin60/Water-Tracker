import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Main page setup
st.markdown("# Water Usage Tracker 💧")
st.sidebar.markdown("# Main page 🎈")

# Intro message
message = "This page provides a water tracking template for Streamlit UI components! 🎉\n"
message += "Please use the sliders below to track your water usage and view the estimated cost report."
st.write(message)

# Water usage input section
st.subheader("Enter Your Daily Water Usage")

# Define the water usage categories and their approximate gallons per use
water_usage_categories = {
    "Shower (minutes)": 2,  # approx. 2 gallons per minute
    "Dishwashing Sessions": 6,  # approx. 6 gallons per session
    "Garden Watering (minutes)": 8,  # approx. 8 gallons per minute
    "Toilet Flushes": 1.6  # approx. 1.6 gallons per flush
}

# Sliders for each category and user input
total_usage = 0
usage_data = {}

with st.form("water_usage_form"):
    for activity, gallons_per_unit in water_usage_categories.items():
        usage = st.slider(f"{activity}", min_value=0, max_value=60 if "minutes" in activity else 20, step=1)
        usage_data[activity] = usage * gallons_per_unit
        total_usage += usage_data[activity]
    
    submitted = st.form_submit_button("Generate Report")

# Generate Financial Report based on usage
if submitted:
    st.subheader("Daily Water Usage Report")
    st.write("Here is a breakdown of your daily water usage:")

    # Show detailed breakdown
    breakdown_df = pd.DataFrame(list(usage_data.items()), columns=["Activity", "Gallons Used"])
    st.table(breakdown_df)

    # Calculate estimated cost
    cost_per_gallon = 0.004  # Approximate cost per gallon in USD
    estimated_cost = total_usage * cost_per_gallon

    st.write(f"**Total Water Usage**: {total_usage:.2f} gallons")
    st.write(f"**Estimated Daily Cost**: ${estimated_cost:.2f}")
    st.write(f"**Estimated Monthly Cost**: ${(estimated_cost * 30):.2f}")
    st.write(f"**Estimated Yearly Cost**: ${(estimated_cost * 365):.2f}")

    # Improvement suggestions
    st.subheader("Suggestions to Reduce Water Usage")
    if usage_data["Shower (minutes)"] > 20:
        st.write("💡 Try reducing your shower time by 5 minutes to save up to 10 gallons.")
    if usage_data["Garden Watering (minutes)"] > 15:
        st.write("💡 Water your garden in the early morning or late evening to reduce evaporation.")
    if usage_data["Dishwashing Sessions"] > 3:
        st.write("💡 Consider washing full loads to reduce water usage.")

    # Generate synthetic data for trend analysis
    st.subheader("Water Usage Trend Over Time")
    
    # Simulate 30 days of water usage data
    dates = pd.date_range(end=datetime.datetime.today(), periods=30).to_pydatetime().tolist()
    synthetic_usage = np.random.normal(loc=total_usage, scale=5, size=30).clip(min=0)  # Simulate around user's total usage

    # Create a DataFrame for the trend data
    trend_data = pd.DataFrame({
        "Date": dates,
        "Daily Water Usage (gallons)": synthetic_usage
    })
    
    # Check data to ensure values are correct
    st.write(trend_data)  # Display data to verify

    # Display line chart of the usage trend
    st.line_chart(trend_data.set_index("Date")["Daily Water Usage (gallons)"])

    st.write("The chart above shows a simulated trend of your water usage over the past 30 days.")
