# 2_Insights_And_AI_Suggestions.py
import streamlit as st
import pandas as pd
import openai

# Function for Generative AI Suggestions
def get_completion(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a knowledgeable and resourceful water-saving advisor specializing in practical and sustainable solutions for individuals and families. Your role involves assessing water usage patterns, identifying areas for improvement, and providing tailored recommendations to help reduce water consumption. You have expertise in various water-saving technologies, landscaping techniques, and behavioral strategies. Additionally, you are skilled at educating clients about the  financial benefits of water conservation. Your goal is to empower clients with actionable advice that is both effective and easy to implement, ultimately promoting a more sustainable approach to water usage."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Water-themed UI styling
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

# Display Insights and Suggestions only if data is available
if "data" in st.session_state:
    st.markdown('<h1 class="main-title">💧 Additional Insights and AI Suggestions</h1>', unsafe_allow_html=True)
    st.sidebar.markdown("# Insights & Suggestions 🌟")

    data = st.session_state["data"]
    household_size = st.session_state["household_size"]
    city = st.session_state["city"]
    total_usage = st.session_state["total_usage"]
    savings_goal = st.session_state["savings_goal"]
    advice_style = st.session_state["advice_style"]

    # Comparison with Household Averages
    st.markdown('<div class="section-title">Household Usage Comparison</div>', unsafe_allow_html=True)
    avg_usage_by_household_size = {
        1: 50, 2: 90, 3: 120, 4: 150, 5: 180
    }
    avg_for_household_size = avg_usage_by_household_size.get(household_size, 100)
    st.write(f"**Comparison**: The average water usage for a {household_size}-person household is approximately {avg_for_household_size} gallons per day.")
    if total_usage > avg_for_household_size:
        st.write("Your water usage is **above average** compared to similar households. Consider implementing water-saving measures.")
    else:
        st.write("Your water usage is **below average** compared to similar households. Keep up the good work!")

    # Generative AI Suggestions for Water Savings
    st.markdown('<div class="section-title">Personalized AI-Generated Water-Saving Suggestions</div>', unsafe_allow_html=True)
    prompt = (
        f"I have a household with {household_size} people located in {city}. "
        f"Our daily water usage is around {total_usage:.2f} gallons. "
        f"We want to save ${savings_goal:.2f} on our water bill. "
        f"The user prefers '{advice_style}' advice. "
        "Please provide some personalized suggestions to help us reduce our water usage and achieve this savings goal."
    )
    suggestions = get_completion(prompt)
    st.write(suggestions)
else:
    st.warning("No data available. Please go to the main page to input details and generate a report.")
