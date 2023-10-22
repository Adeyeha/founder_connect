import sys
sys.path.append(r'utils')
import streamlit as st
# Set page configuration
st.set_page_config(
    page_title="Explore Startups", 
    page_icon="🔍", 
    layout="centered"
)

import pandas as pd
from options import *
import db
from options import *
from templates import user_signed_in, confirm_investor_user
import helpers
from streamlit_extras.switch_page_button import switch_page 

helpers.add_investor_pages()

def explore_page():

    user_signed_in()
    confirm_investor_user()

    st.title("Explore Startup Profiles ")

    # Filtering options
    with st.sidebar:
        st.header("Filter Options")
        startup_stage_filter = st.multiselect("Startup Stage", STARTUP_STAGES)
        country_filter = st.multiselect("Country(s)", COUNTRIES)
        industry_filter = st.multiselect("Industry", INDUSTRIES)
        
        # Use sliders for investment and age filters
        investment_needed_range = st.slider("Investment Needed ($)", min_value=0, max_value=2000000, value=(0, 1000000))
        min_investment_needed_filter, max_investment_needed_filter = investment_needed_range[0], investment_needed_range[1]
        
        startup_age_filter = st.slider("Startup Age", min_value=0, max_value=20, value=(0, 10))

    # Fetch all startup profiles (or apply filters as needed)
    startup_profiles = db.get_startups()  # Assuming get_startups is a function to fetch startup data

    # Apply filters
    if startup_stage_filter:
        startup_profiles = [profile for profile in startup_profiles if profile['startup_stage'] in startup_stage_filter]
    if country_filter:
        startup_profiles = [profile for profile in startup_profiles if any(item in country_filter for item in profile['startup_countries'].split())]
    if industry_filter:
        startup_profiles = [profile for profile in startup_profiles if any(item in industry_filter for item in profile['startup_industries'])]
    if min_investment_needed_filter:
        startup_profiles = [profile for profile in startup_profiles if profile['investment_needed'] >= min_investment_needed_filter]
    if max_investment_needed_filter:
        startup_profiles = [profile for profile in startup_profiles if profile['investment_needed'] <= max_investment_needed_filter]
    if startup_age_filter:
        startup_profiles = [profile for profile in startup_profiles if startup_age_filter[0] <= profile['startup_age'] <= startup_age_filter[1]]


    # Convert list of dictionaries to DataFrame and display
    df = pd.DataFrame(startup_profiles)
    st.dataframe(df)
    col1,col2,col3 = st.columns(3)
    back = col2.button("Personalized Recommendations") 
    if back:
        switch_page("Recommend_Startups")

if __name__ == "__main__":
    explore_page()
