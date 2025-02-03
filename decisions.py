import streamlit as st
import pandas as pd
from datetime import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOOD_LOG_FILE = os.path.join(SCRIPT_DIR, "mood_log.xlsx")
WELLBEING_LOG_FILE = os.path.join(SCRIPT_DIR, "wellbeing_log.xlsx")

def create_excel_file(filename, columns):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_excel(filename, index=False, engine="openpyxl")
        print(f"✅ Created file: {filename}")

def append_to_excel(data, filename):
    df_new = pd.DataFrame([data]) 

    if os.path.exists(filename):
        df_existing = pd.read_excel(filename, engine="openpyxl")
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(filename, index=False, engine="openpyxl")
    print(f"✅ Data saved to: {filename}")

    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")

create_excel_file(MOOD_LOG_FILE, ["Date", "Time", "Activity", "Mood", "Mood Score", "Agitation Level", "Energy Level", "Motivation Level"])
create_excel_file(WELLBEING_LOG_FILE, ["Date", "Elvanse Intake", "Location", "Guitar Hours", "Wellbeing Score", "Exercised Hours", "Model Hours", "Worked Hours", "Studied Hours", "Time Outside", "Social Interaction", "Estimated Social Hours", "Externality Impact", "Externality Category", "Externality Description"])    


# ---- Custom CSS Styling ----
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400&family=Lora:wght@300;400&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Lora', serif;
        background-color: #E3EAFD !important; /* Soft pastel blue */
        color: #a062d1 !important; /* Darker text for readability */
    }  

    .title {
        text-align: center;
        color: #b274e3;  /* Lilac */
        font-size: 48px;
        font-weight: 300;
        padding: 20px 0;
        font-family: 'Playfair Display', serif;
    }

    .main-content {
        background-color: rgba(227, 234, 253, 0.9); /* Softer pastel blue with transparency */
        padding: 30px;
        border-radius: 15px;
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1);
    }

    div[data-baseweb="slider"] > div:first-child > div {
        background-color: #6A5ACD !important; /* Soft dark lavender knob */
        border-color: #9370DB !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Current Activity & Mood", "General Wellbeing"])

st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

if page == "Current Activity & Mood":
    st.header("Log your current activity and mood")

    activity_status = st.selectbox("Current activity status:", 
                                   ["Working on project","Working for Institute", "Finished working for institute", "Finished giving a private lesson",  "Studying", "Finished studying", "Exercising", "Finished exercising", "Playing the guitar", "Finished playing the guitar", "Hearing podcast", "Hearing audibook or reading book", "Doing administrate task", "Meeting friends", "Socializing with flatmates", "Going to bandpractice", "Finished band practice", "Using social media", "Finished using social media", "Consuming news", "Engaging with internal thought", "Going for a walk", "Finished therapy","Other"])
    if activity_status == "Other":
        activity = st.text_input("Please specify your current activity:")

    mood = st.selectbox("Mood:", 
                        ["Happy", "Pleased", "Enthusiastic", "Curious", "Relieved", "Hopeful", "Neutral", "Bothered", "Anxious", "Irritated", "Stressed", "Frustrated", "Unfocused", "Neutral", "Overwhelmed", "Sick"])
    mood_score = st.slider("Mood score (0 = very bad, 10 = very good)", 0.0, 10.0, 5.0, step=0.5)
    agitation_level = st.slider("Agitation Level (0 = calm, 10 = highly agitated)", 0.0, 10.0, 5.0, step=0.5)
    energy_level = st.slider("Physiological Energy Level (0 = exhausted, 10 = very energetic)", 0.0, 10.0, 5.0, step=0.5)
    motivation_level = st.slider("Motivation Level (0 = no motivation, 10 = very motivated)", 0.0, 10.0, 5.0, step=0.5)
    selected_date = st.date_input("Date", datetime.today().date())
    selected_time = st.time_input("Time")
    
    if st.button("Log Activity & Mood"):
        data = {
            "Date": selected_date,
            "Time": selected_time,
            "Activity": activity_status if activity_status != "Other" else activity,
            "Mood": mood,
            "Mood Score": mood_score,
            "Agitation Level": agitation_level,
            "Energy Level": energy_level,
            "Motivation Level": motivation_level
        }
        append_to_excel(data, MOOD_LOG_FILE)
        st.success("Activity & Mood logged successfully!")

elif page == "General Wellbeing":
    st.write("Overall Wellbeing Tracker")
    st.header("Log your general wellbeing")
    selected_date = st.date_input("Select the date you're tracking the data for:", datetime.today().date())
    elvanse_intake = st.selectbox("Did you take Elvanse today?", ["Yes", "No"])
    location = st.selectbox("Location", ["Bonn", "Away", "Other"])
    minutes_guitar = st.slider("How many hours did you play the guitar today?", 0.0, 10.0, 0.0, step=0.25)
    wellbeing_score = st.slider("Wellbeing score", 0.0, 10.0, 0.0, step=0.5)
    exercised = st.slider("How many hours did you exercise today?", 0.0, 10.0, 0.0, step=0.25)
    hours_model = st.slider("How many hours did you work on the decision model today?", 0.0, 10.0, 0.0, step=0.25)
    hours_worked = st.slider("How many hours did you work today?", 0.0, 10.0, 0.0, step=0.25)
    hours_studied = st.slider("How many hours did you study today?", 0.0, 10.0, 0.0, step=0.25)
    time_outside = st.selectbox("Did you leave the house today?",
                                ["No", "Went to the supermarket", "Ran errands in the city", "Met friends outside", "Went to the gym", "Went for a walk", "Went to the library", "Went to university", "Gave private lesson", "Went to the office", "Went to appointment", "Travelling"])
    social_interaction = st.multiselect("What kind of physical social interaction did you have today?", 
                                        ["Through work giving private lesson", "Through work at institute", "Met with friend/friends", "No significant one, only online interaction", "No significant social interaction", "None"])
    estimated_time_social_interaction = st.slider("How many hours did you spend socializing?", 0.0, 10.0, 0.0, step=0.25)
    externality_impact = st.selectbox("Did any event happen today that had an impact on your mood?", ["Yes", "No"])
    if externality_impact == "Yes":
        externality_category = st.selectbox("Select the category of the event:",
                                            ["Work-related", "Academic", "Romantic", "Social", "Health", "Family-related", "Other"])
        externality_description = st.text_area("Describe the event that impacted your mood:")
    else:
        externality_category = None
        externality_description = None
    if st.button("Log wellbeing data"):
        data = {
            "Date": selected_date,
            "Elvanse Intake": elvanse_intake,
            "Location": location,
            "Guitar Hours": minutes_guitar,
            "Wellbeing Score": wellbeing_score,
            "Exercised Hours": exercised,
            "Model Hours": hours_model,
            "Worked Hours": hours_worked,
            "Studied Hours": hours_studied,
            "Time Outside": time_outside,
            "Social Interaction": ", ".join(social_interaction),
            "Estimated Social Hours": estimated_time_social_interaction,
            "Externality Impact": externality_impact,
            "Externality Category": externality_category,
            "Externality Description": externality_description
        }
        append_to_excel(data, WELLBEING_LOG_FILE)
        st.success("Wellbeing data logged successfully!")

st.markdown("</div>", unsafe_allow_html=True)        