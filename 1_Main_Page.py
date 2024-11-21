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
    "Campbell": "Pages/Data/Campbell_Water_Usage1.csv",
    "Cupertino": "Pages/Data/Cupertino_Water_Usage1.csv",
    "Gilroy": "Pages/Data/Gilroy_Water_Usage1.csv",
    "Los Altos": "Pages/Data/Los_Altos_Water_Usage.csv",
    "Los Altos Hills": "Pages/Data/Los_Altos_Hills_Water_Usage.csv",
    "Los Gatos": "Pages/Data/Los_Gatos_Water_Usage.csv",
    "Milpitas": "Pages/Data/Milpitas_Water_Usage1.csv",
    "Monte Sereno": "Pages/Data/Monte_Sereno_Water_Usage.csv",
    "Morgan Hill": "Pages/Data/Morgan_Hill_Water_Usage.csv",
    "Mountain View": "Pages/Data/Mountain_View_Water_Usage.csv",
    "Palo Alto": "Pages/Data/Palo_Alto_Water_Usage.csv",
    "San Jose": "Pages/Data/San_Jose_Water_Usage.csv",
    "San Martin": "Pages/Data/San_Martin_Water_Usage.csv",
    "Santa Clara": "Pages/Data/Santa_Clara_Water_Usage.csv",
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

#Adding logo to top of the page
def add_logo():
    logo_path = "Pages/logo/logo.png"
    st.markdown(
        f"""
        <style>
            .logo-container {{
                text-align: center;
                margin-top: -125px; /* Adjust this to reduce top white space */
                margin-bottom: -125px; /* Adjust this to reduce bottom white space */
            }}
            .logo-container img {{
                width: 300px; /* Adjust size to your preference */
                border-radius: 10%;
            }}
        </style>
        <div class="logo-container">
            <img src="data:image/png;base64,{convert_image_to_base64(logo_path)}" alt="Logo">
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

# Call the function to add the logo
add_logo()

#Selection menu
st.markdown('<div class="section-title">Enter Household Details</div>', unsafe_allow_html=True)
household_size = st.number_input("Number of people in household", min_value=1, step=1)
city = st.selectbox("Choose a city:", list(city_files.keys()))
savings_goal = st.number_input("Savings goal (USD):", min_value=0.0, step=1.0)
total_usage = data["Total Usage (gallons)"].mean()

#Start of website
if st.button("Proceed to Report"):    
    st.session_state["household_size"] = household_size
    st.session_state["city"] = city
    st.session_state["savings_goal"] = savings_goal
    st.success("Details saved! Navigate to 'View Report' for analysis.")
    st.session_state["data"] = data
    st.session_state["total_usage"] = total_usage

    avg_usage_by_household_size = {
        1: 1, 2: 2, 3: 2.5, 4: 2.75, 5: 3
    }

    big_household = {
        5: 5, 0.1: 0.1, 3: 3
        }

    # Check if household size is within the predefined range or requires calculation
    if household_size in avg_usage_by_household_size:
        avg_for_household_size = avg_usage_by_household_size[household_size]
    else:
        # Calculate average usage for household sizes greater than 5
        avg_for_household_size = (((household_size - big_household[5]) * big_household[0.1]) + big_household[3])

    st.session_state["avg_for_household_size"] = avg_for_household_size

#elif step == "View Report":
#st.markdown('<div class="section-title">Daily Water Usage Report</div>', unsafe_allow_html=True)

if "city" in st.session_state:
    avg_for_household_size = st.session_state["avg_for_household_size"]
    data_path = city_files[st.session_state["city"]]
    city_data = pd.read_csv(data_path)
    numeric_columns = data.select_dtypes(include=[np.number]).columns

    # Calculate average usage
    avg_usage = data[numeric_columns].mean().to_dict()
    avg_usage.pop("Total Usage (gallons)", None)

    # Display table
    avg_usage_df = pd.DataFrame(list(avg_usage.items()), columns=["Activity", "Average Daily Gallons"])
    st.write("Here is your average daily water usage for each activity:")
    st.table(avg_usage_df)

    # Calculate city average usage
    city_avg_usage = city_data[numeric_columns].mean().to_dict()
    city_avg_usage.pop("Total Usage (gallons)", None)
    comparison_df = pd.DataFrame({
        "Activity": avg_usage_df["Activity"],
        "Your Usage (gallons)": avg_usage_df["Average Daily Gallons"] * avg_for_household_size,
        "City Average (gallons)": [city_avg_usage.get(activity, 0) * avg_for_household_size for activity in avg_usage_df["Activity"]]

    })


    # Dropdown menu for cost calculations
    st.markdown('<div class="section-title">Estimated Water Costs</div>', unsafe_allow_html=True)

    # Select bar chart to view
    cost_chart_choice = st.selectbox(
        "Select a cost graph to view:",
        ["Estimated Daily Cost", "Estimated Monthly Cost", "Estimated Yearly Cost"],
        key="cost_chart_choice"
    )

    # Define cost parameters
    cost_per_gallon = 0.1  # Cost per gallon in USD
    total_usage = data["Total Usage (gallons)"].mean()
    estimated_cost_daily = total_usage * cost_per_gallon * avg_for_household_size
    estimated_cost_monthly = estimated_cost_daily * 30
    estimated_cost_yearly = estimated_cost_daily * 365

    # Calculate city-specific costs
    city = st.session_state["city"]
    city_data = pd.read_csv(city_files[city])
    total_usage_city = city_data["Total Usage (gallons)"].mean()
    estimated_cost_daily_city = total_usage_city * cost_per_gallon * avg_for_household_size
    estimated_cost_monthly_city = estimated_cost_daily_city * 30
    estimated_cost_yearly_city = estimated_cost_daily_city * 365

    # Prepare data for plotting
    costs = {
        "Estimated Daily Cost": [estimated_cost_daily, estimated_cost_daily_city],
        "Estimated Monthly Cost": [estimated_cost_monthly, estimated_cost_monthly_city],
        "Estimated Yearly Cost": [estimated_cost_yearly, estimated_cost_yearly_city]
    }
    labels = ["Your Average", f"{city} Average"]

    # Generate bar plot for selected cost graph
    fig_cost = px.bar(
        y=labels,
        x=costs[cost_chart_choice],
        orientation='h',  # Horizontal bar chart
        title=f"{cost_chart_choice} Comparison",
        labels={"y": "Type", "x": "Cost in USD"},
        color=labels,
        color_discrete_map={"Your Average": "#1E88E5", f"{city} Average": "#FF7F0E"},
        text=costs[cost_chart_choice]  # Add cost values as labels
    )

    # Update trace to increase text size and add bold font
    fig_cost.update_traces(
        texttemplate='<b>$%{text:.2f}</b>',
        textposition='outside',
        textfont=dict(size=20)
    )

    # Update layout for better readability
    fig_cost.update_layout(
    title=dict(text=f"{cost_chart_choice} Comparison",font=dict(size=20)),
    xaxis=dict(title="Cost in USD",titlefont=dict(size=16),tickfont=dict(size=14), range=[0, max(costs[cost_chart_choice]) * 1.3]),
    yaxis=dict(title="",tickfont=dict(size=16)),
    width=1000,  # Set the width of the chart
    height=300,  # Set the height of the chart
    margin=dict(l=50, r=120, t=50, b=50),
    legend_title=dict(text="") # Remove "color" text from legend title
    )

    # Display cost graph
    st.plotly_chart(fig_cost)
    
    # Generate AI insights for cost analysis
    ai_prompt_cost_insights = (
        f"In {city}, the water cost comparison shows that your household incurs "
        f"{cost_chart_choice.lower()} of ${costs[cost_chart_choice][0]:.2f}, "
        f"while the city average for a household of similar size is ${costs[cost_chart_choice][1]:.2f}. "
        f"Analyze the potential reasons for these differences in cost between {total_usage*avg_for_household_size:.2f} and {total_usage_city*avg_for_household_size:.2f} and provide actionable strategies "
        "to reduce your household's water expenses without compromising necessary usage."
    )

    # Fetch AI-generated insights
    ai_cost_insights = get_completion(ai_prompt_cost_insights)

    # Create Collapsible Section for AI-Powered Cost Insights
    with st.expander("AI-Powered Cost Insights"):
        st.write(f"**Comparison**: **The average water usage for a {household_size}-person household in {city} is approximately {total_usage_city*avg_for_household_size:.2f} gallons per day.**")
        if total_usage > avg_for_household_size:
            st.write("Your water usage is ***above average*** compared to similar households. Consider implementing water-saving measures.")
        else:
            st.write("Your water usage is ***below average*** compared to similar households. Keep up the good work!")
        st.write(ai_cost_insights)


    # Generate AI-powered recommendations for cost reduction
    ai_prompt_cost_recommendations = (
        f"Based on the selected cost graph ({cost_chart_choice}) for your household in {city}, "
        "suggest specific measures to reduce water costs. Focus on high-impact, cost-effective actions "
        "such as adjusting habits, using efficient appliances, or optimizing systems."
    )

    # Fetch AI recommendations
    ai_cost_recommendations = get_completion(ai_prompt_cost_recommendations)

    # Create Collapsible Section for AI-Powered Cost Reduction Recommendations
    with st.expander("AI-Powered Cost Reduction Recommendations"):
        st.write(ai_cost_recommendations)



    # Generate AI Insights: Prompt for Analysis
    ai_prompt_comparison = (
        f"In {st.session_state['city']}, we compared the average daily water usage of your household to the city averages "
        f"for the following activities: {', '.join(comparison_df['Activity'])}. "
        f"Your household uses {avg_usage_df['Average Daily Gallons'].sum():.2f} gallons per day, while the city average is "
        f"{sum(comparison_df['City Average (gallons)']):.2f} gallons per day for a household of similar size. "
        f"Please analyze these differences and provide actionable insights to reduce water consumption where your usage is above average."
    )
    ai_comparison_insights = get_completion(ai_prompt_comparison)

    # Create Collapsible Section for AI-Powered Insights on Usage Comparison
    with st.expander("AI-Powered Insights on Usage Comparison"):
        st.write(ai_comparison_insights)

    # Generate and display comparison chart
    st.markdown('<div class="section-title">Comparison of Your Usage vs. City Average</div>', unsafe_allow_html=True)
    fig_comparison = px.bar(
        comparison_df,
        x="Activity",
        y=["Your Usage (gallons)", "City Average (gallons)"],
        barmode="group",
        title="Daily Water Usage Comparison (in Gallons)",
        labels={"value": "", "variable": "Type"},
        color_discrete_map={"Your Usage (gallons)": "#1E88E5", "City Average (gallons)": "#FF7F0E",}
    )

    # Adjust the size of the figure
    fig_comparison.update_layout(
        width=900,  # Set the width of the chart
        height=450,  # Set the height of the chart
        title=dict(font=dict(size=16)),  # Adjust title font size if needed
        margin=dict(l=50, r=50, t=50, b=50),  # Adjust margins to reduce whitespace
        legend_title=dict(text=""), # Remove "type" text from legend title
        xaxis_title= ""  # Remove "Activity" text from the x-axis
    )
    
    #Displaying & Centering the Chart
    st.plotly_chart(fig_comparison)
    

    # Generate AI Insights: Recommendations
    ai_prompt_recommendations = (
        f"Based on the water usage comparison chart for your household in {st.session_state['city']}, "
        f"provide specific recommendations for each activity where your usage exceeds the city average. "
        "Include practical actions to reduce water consumption for each of these activities."
    )
    ai_recommendations = get_completion(ai_prompt_recommendations)

    # Create Collapsible Section for AI-Powered Recommendations for Reducing Usage
    with st.expander("AI-Powered Recommendations for Reducing Usage"):
        st.write(ai_recommendations)

    # Water Trend Over Time
    st.markdown('<div class="section-title">Water Usage Trends Graph</div>', unsafe_allow_html=True)
    data['Date'] = pd.to_datetime(data['Date'])
    city_data['Date'] = pd.to_datetime(city_data['Date'])

    data.set_index('Date', inplace=True)
    city_data.set_index('Date', inplace=True)

    trend_data_combined = pd.DataFrame({
        'Your Usage (gallons)': data['Total Usage (gallons)'] * avg_for_household_size,
        'City Average (gallons)': city_data['Total Usage (gallons)'] * avg_for_household_size
    })
    
    # Creating the figure 
    fig = px.line(
    trend_data_combined,
    x=trend_data_combined.index,
    y=['Your Usage (gallons)', 'City Average (gallons)'],
    labels={
        "value": "Usage (gallons)",
        "variable": "",
        "index": ""
    },
    title="Water Usage Trend Over Time (in Gallons)", 
    color_discrete_map={"Your Usage (gallons)": "#1E88E5", "City Average (gallons)": "#FF7F0E",}
    )

    # Customize layout
    fig.update_layout(
    template='plotly_white',
    xaxis_title="", # Remove "Date" text from the x-axis 
    yaxis_title="", # Remove "Gallons" text from the y-axis
    xaxis=dict(
        tickformat="%b %d %Y",  # Format: "Month Day Year" (e.g., Oct 4 2024)
        showgrid=True #Shows vertical grid lines for better readability
        )
    )

    # Make the lines thicker
    fig.update_traces(line=dict(width=3))  # Set line thickness to 3
    
    # Render the Plotly figure in Streamlit
    st.plotly_chart(fig)

else:
    st.warning("No data available. Please go to the main page to input details and generate a report.")    