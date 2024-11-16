# Improved 1_Main_Page.py with Enhanced UI/UX
import streamlit as st
import pandas as pd
import numpy as np
import openai
import os
import matplotlib.pyplot as plt
import plotly.express as px

# Load datasets
data = pd.read_csv('Pages/Data/Synthetic Water Usage.csv')
city_files = {
    "L.A. Hills": "Pages/Data/L.A._Hills_Water_Usage.csv",
    "Palo Alto": "Pages/Data/Palo_Alto_Water_Usage.csv",
    "Mountain View": "Pages/Data/Mountain_View_Water_Usage.csv",
    "Los Altos": "Pages/Data/Los_Altos_Water_Usage.csv",
    "Santa Clara": "Pages/Data/Santa_Clara_Water_Usage.csv",
    "San Jose": "Pages/Data/San_Jose_Water_Usage.csv",
    "Monte Sereno": "Pages/Data/Monte_Sereno_Water_Usage.csv",
    "Los Gatos": "Pages/Data/Los_Gatos_Water_Usage.csv",
    "Morgan Hill": "Pages/Data/Morgan_Hill_Water_Usage.csv",
    "Campbell": "Pages/Data/Campbell_Water_Usage1.csv",
    "Cupertino": "Pages/Data/Cupertino_Water_Usage1.csv",
    "Gilroy": "Pages/Data/Gilroy_Water_Usage1.csv",
    "Milpitas": "Pages/Data/Milpitas_Water_Usage1.csv",
    "San Martin": "Pages/Data/San_Martin_Water_Usage.csv",
    "Saratoga": "Pages/Data/Saratoga_Water_Usage1.csv",
    "Sunnyvale": "Pages/Data/Sunnyvale_Water_Usage1.csv"
}

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_completion(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a resourceful water-saving advisor providing actionable water-saving advice."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=750,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()
import streamlit as st

def add_logo():
    logo_path = "Pages/logo/logo.png"  # Update this path based on your project structure
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{convert_image_to_base64(logo_path)}" alt="Logo" style="width: 500px; border-radius: 10%;">
        </div>
        """,
        unsafe_allow_html=True
    )

def convert_image_to_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


    

# Thematic styling
st.set_page_config(page_title="💧 Water Usage Tracker", layout="wide")
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5em;
            color: #1E88E5;
            font-weight: bold;
            text-align: center;
            padding: 1em 0;
        }
        .section-title {
            font-size: 1.8em;
            color: #0277BD;
            font-weight: bold;
            padding-top: 1em;
        }
        .sidebar .sidebar-content {
            background-color: #E3F2FD;
        }
    </style>
""", unsafe_allow_html=True)

# Call the function to add the logo to the sidebar
add_logo()


# Multi-step navigation
step = st.sidebar.radio("Navigation:", ["Enter Details", "View Report", "Insights"])

if step == "Enter Details":
    st.markdown('<div class="section-title">Enter Household Details</div>', unsafe_allow_html=True)
    household_size = st.number_input("Number of people in household", min_value=1, step=1)
    city = st.selectbox("Choose a city:", list(city_files.keys()))
    advice_style = st.radio("Select the style of advice:", ["Concise tips", "Detailed advice", "Friendly reminders"])
    savings_goal = st.number_input("Savings goal (USD):", min_value=0.0, step=1.0)
    total_usage = data["Total Usage (gallons)"].mean()

    if st.button("Proceed to Report"):
        st.session_state["household_size"] = household_size
        st.session_state["city"] = city
        st.session_state["advice_style"] = advice_style
        st.session_state["savings_goal"] = savings_goal
        st.success("Details saved! Navigate to 'View Report' for analysis.")
        st.session_state["data"] = data
        st.session_state["total_usage"] = total_usage

        avg_usage_by_household_size = {
            1: 1, 2: 2, 3: 2.5, 4: 2.75, 5: 3
        }
        # Check if household size is within the predefined range or requires calculation
        if household_size in avg_usage_by_household_size:
            avg_for_household_size = avg_usage_by_household_size[household_size]
        else:
            # Calculate average usage for household sizes greater than 5
            avg_for_household_size = (((household_size - 5) * 0.1) + 3)

        st.session_state["avg_for_household_size"] = avg_for_household_size

elif step == "View Report":
    st.markdown('<div class="section-title">Daily Water Usage Report</div>', unsafe_allow_html=True)
    
    if "city" in st.session_state:
        avg_for_household_size = st.session_state["avg_for_household_size"]
        data_path = city_files[st.session_state["city"]]
        lower_data = pd.read_csv(data_path)
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        avg_usage = data[numeric_columns].mean().to_dict()
        avg_usage.pop("Total Usage (gallons)", None)

        # Display table
        avg_usage_df = pd.DataFrame(list(avg_usage.items()), columns=["Activity", "Average Daily Gallons"])
        st.write("Here is your average daily water usage for each activity:")
        st.table(avg_usage_df)

        city_avg_usage = lower_data[numeric_columns].mean().to_dict()
        city_avg_usage.pop("Total Usage (gallons)", None)
        comparison_df = pd.DataFrame({
            "Activity": avg_usage_df["Activity"],
            "Your Usage (gallons)": avg_usage_df["Average Daily Gallons"],
            "City Average (gallons)": [city_avg_usage.get(activity, 0) * avg_for_household_size for activity in avg_usage_df["Activity"]]
        })

        # Comparison Chart
        st.markdown('<div class="section-title">Comparison of Your Usage vs. City Average</div>', unsafe_allow_html=True)
        fig_comparison = px.bar(
            comparison_df,
            x="Activity",
            y=["Your Usage (gallons)", "City Average (gallons)"],
            barmode="group",
            title="Daily Water Usage Comparison",
            labels={"value": "Gallons", "variable": "Type"},
        )
        st.plotly_chart(fig_comparison)

        # Cost Calculations
        st.markdown('<div class="section-title">Estimated Water Costs</div>', unsafe_allow_html=True)
        cost_per_gallon = 0.1
        total_usage = data["Total Usage (gallons)"].mean()
        estimated_cost_daily = total_usage * cost_per_gallon
        estimated_cost_monthly = estimated_cost_daily * 30
        estimated_cost_yearly = estimated_cost_daily * 365

        st.metric("Daily Cost", f"${estimated_cost_daily:.2f}")
        st.metric("Monthly Cost", f"${estimated_cost_monthly:.2f}")
        st.metric("Yearly Cost", f"${estimated_cost_yearly:.2f}")

        # Water Trend Over Time
        st.markdown('<div class="section-title">Water Usage Trend Over Time</div>', unsafe_allow_html=True)
        data['Date'] = pd.to_datetime(data['Date'])
        lower_data['Date'] = pd.to_datetime(lower_data['Date'])

        data.set_index('Date', inplace=True)
        lower_data.set_index('Date', inplace=True)

        trend_data_combined = pd.DataFrame({
            'Your Usage (gallons)': data['Total Usage (gallons)'],
            'City Average (gallons)': lower_data['Total Usage (gallons)']
        })

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

elif step == "Insights":
    st.markdown('<div class="section-title">Personalized Insights and AI Suggestions</div>', unsafe_allow_html=True)

    if "data" in st.session_state:
        # Retrieve stored session data
        data = st.session_state["data"]
        household_size = st.session_state["household_size"]
        city = st.session_state["city"]
        total_usage = st.session_state["total_usage"]

        savings_goal = st.session_state["savings_goal"]
        advice_style = st.session_state["advice_style"]
        avg_for_household_size = st.session_state["avg_for_household_size"]

        # Comparison with Household Averages
        st.markdown('<div class="section-title">Household Usage Comparison</div>', unsafe_allow_html=True)

        st.write(f"**Comparison**: The average water usage for a {household_size}-person household is approximately {avg_for_household_size:.2f} gallons per day.")
        if total_usage > avg_for_household_size:
            st.write("Your water usage is **above average** compared to similar households. Consider implementing water-saving measures.")
        else:
            st.write("Your water usage is **below average** compared to similar households. Keep up the good work!")

        # Generative AI Suggestions for Water Savings
        st.markdown('<div class="section-title">Personalized AI-Generated Water-Saving Suggestions</div>', unsafe_allow_html=True)
        prompt = (
            f"I have a household with {household_size} people. "
            f"Our daily water usage is around {total_usage:.2f} gallons. "
            f"We want to save ${savings_goal:.2f} on our water bill. "
            f"The user prefers '{advice_style}' advice. "
            "Based on the my water usage statistics, please provide a detailed analysis of what causes the high household water consumption for me. "
            "Also be sure to include my water usage amount, as well as the price. "
            "In this analysis, identify the high usage areas. "
            "For the analysis, use the following template for what to say:\n"
            "'Based on your current water usage of ___ gallons per day and your goal to save $___ on your water bill, here are some concise tips to help you achieve your water-saving and cost-saving goals:'\n"
            "Following this analysis, provide recommendations on how to save water in each high usage problem area based on the average daily water usage by activity graph on the first page of the application. "
            "Consider factors such as my family size, lifestyle habits, and common appliances in use. "
            "It is also important to take into account my data on water usage and prices and compare it to the selected city's average to determine which of my activities is above average and create personalized recommendations to reduce water usage. "
            "Please include practical suggestions such as changes in daily routines that can be adopted to reduce water usage effectively. "
            "You should have the following headers: **Analysis of High Household Water Consumption**, **Identified High Usage Areas**, **Recommendations for Water Savings**, and **Additional Tips for Water Savings**. "
            "Be sure to increase the size of these headers and make them bold."
        )
        suggestions = get_completion(prompt)
        st.write(suggestions)
    else:
        st.warning("No data available. Please go to the main page to input details and generate a report.")

