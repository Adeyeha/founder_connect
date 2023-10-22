import sys
sys.path.append(r'utils')
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Explore Investors", 
    page_icon="🔍", 
    layout="centered"
)

import pandas as pd
import db
from options import *
from templates import user_signed_in,confirm_startup_user
import helpers
from streamlit_extras.switch_page_button import switch_page 

helpers.add_startup_pages()

def explore_page():

    user_signed_in()
    confirm_startup_user()

    st.title("Explore Investor Profiles 💼")

    # Filtering options
    with st.sidebar:
        st.header("Filter Options")
        investor_type_filter = st.multiselect("Investor Type", INVESTOR_TYPES)
        country_filter = st.multiselect("Preferred Country(s)", COUNTRIES)
        industry_filter = st.multiselect("Preferred Industry", INDUSTRIES)
        
        # Use a slider for min and max investment filters
        investment_range = st.slider("Investment Range ($)", min_value=0, max_value=2000000, value=(0, 1000000))
        min_investment_filter, max_investment_filter = investment_range[0], investment_range[1]

    # Fetch all investor profiles (or apply filters as needed)
    investor_profiles = db.get_investors()

    # Apply filters
    if investor_type_filter:
        investor_profiles = [profile for profile in investor_profiles if any(item in investor_type_filter for item in profile['investor_type'])]
    if country_filter:
        investor_profiles = [profile for profile in investor_profiles if any(item in country_filter for item in profile['preferred_country'])]
    if industry_filter:
        investor_profiles = [profile for profile in investor_profiles if any(item in industry_filter for item in profile['preferred_industry'])]
    if min_investment_filter:
        investor_profiles = [profile for profile in investor_profiles if profile['min_investment'] >= min_investment_filter]
    if max_investment_filter:
        investor_profiles = [profile for profile in investor_profiles if profile['max_investment'] <= max_investment_filter]

    # Convert list of dictionaries to DataFrame and display
    df = pd.DataFrame(investor_profiles)
    st.dataframe(df)

    col1,col2,col3 = st.columns(3)
    back = col2.button("Personalized Recommendations") 
    if back:
        switch_page("Recommend_Investors")

if __name__ == "__main__":
    explore_page()
