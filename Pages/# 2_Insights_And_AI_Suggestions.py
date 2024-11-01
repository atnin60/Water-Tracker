# 2_Insights_And_AI_Suggestions.py
import streamlit as st
import pandas as pd
import openai

# Function for Generative AI Suggestions
def get_completion(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a wise old wizard providing water-saving advice."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Display Insights and Suggestions only if data is available
if "user_data" in st.session_state:
    st.markdown("# Additional Insights and AI Suggestions 💧")
    st.sidebar.markdown("# Insights & Suggestions 🌟")
    
    user_data = st.session_state["user_data"]
    household_size = st.session_state["household_size"]
    state = st.session_state["state"]
    total_usage = st.session_state["total_usage"]
    savings_goal = st.session_state["savings_goal"]
    advice_style = st.session_state["advice_style"]

    # Additional Insights
    st.subheader("Additional Insights")
    numeric_columns = user_data.select_dtypes(include=[float, int]).columns
    max_usage_day = user_data[numeric_columns].sum(axis=1).idxmax()
    min_usage_day = user_data[numeric_columns].sum(axis=1).idxmin()
    st.write(f"**Peak Water Usage Day**: {user_data.iloc[max_usage_day]['Date']} with {user_data.iloc[max_usage_day][numeric_columns].sum()} gallons")
    st.write(f"**Lowest Water Usage Day**: {user_data.iloc[min_usage_day]['Date']} with {user_data.iloc[min_usage_day][numeric_columns].sum()} gallons")

    # Comparison with Household Averages
    avg_usage_by_household_size = {
        1: 50, 2: 90, 3: 120, 4: 150, 5: 180
    }
    avg_for_household_size = avg_usage_by_household_size.get(household_size, 100)
    st.write(f"**Comparison**: The average water usage for a {household_size}-person household is approximately {avg_for_household_size} gallons per day.")
    if total_usage > avg_for_household_size:
        st.write(f"Your water usage is **above average** compared to similar households. Consider implementing water-saving measures.")
    else:
        st.write(f"Your water usage is **below average** compared to similar households. Keep up the good work!")

    # Generative AI Suggestions for Water Savings
    st.subheader("Personalized AI-Generated Water-Saving Suggestions")
    prompt = (
        f"I have a household with {household_size} people located in {state}. "
        f"Our daily water usage is around {total_usage:.2f} gallons. "
        f"We want to save ${savings_goal:.2f} on our water bill. "
        f"The user prefers '{advice_style}' advice. "
        "Please provide some personalized suggestions to help us reduce our water usage and achieve this savings goal."
    )
    suggestions = get_completion(prompt)
    st.write(suggestions)
else:
    st.warning("No data available. Please go to the main page to input details and generate a report.")
