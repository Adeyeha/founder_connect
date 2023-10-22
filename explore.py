import streamlit as st
import pandas as pd
from utils.options import *
# Assuming you have the relevant imports for your database connections and functions.
# from database_module import *

def fetch_all_investors():
    """
    Fetches all investor profiles from the database. 
    For now, we'll return dummy data.
    """
    dummy_data = [
        {
            'investment_company': 'ABC Investments',
            'investor_type': 'Angel Investor,VC Fund',
            'preferred_country': 'USA',
            'preferred_business_priority': 'Revenue Growth,Market Share',
            'preferred_founder_gender': 'Female',
            'preferred_investment_round': 'Seed,Series A',
            'preferred_industry': 'Tech,Healthcare',
            'preferred_startup_age': '2-5',
            'preferred_business_model': 'Subscription,SaaS',
            'min_investment': 10000,
            'max_investment': 100000,
        },
        {
            'investment_company': 'XYZ Capital',
            'investor_type': 'Family Office,VC Fund',
            'preferred_country': 'UK',
            'preferred_business_priority': 'User Acquisition,Profitability',
            'preferred_founder_gender': 'Male',
            'preferred_investment_round': 'Series B,Series C',
            'preferred_industry': 'Fintech,Edtech',
            'preferred_startup_age': '5-10',
            'preferred_business_model': 'Marketplace,Ad Revenue',
            'min_investment': 5000,
            'max_investment': 80000,
        },
        {
            'investment_company': 'LMN Ventures',
            'investor_type': 'Angel Investor',
            'preferred_country': 'Nigeria',
            'preferred_business_priority': 'Revenue Growth,User Engagement',
            'preferred_founder_gender': 'Any',
            'preferred_investment_round': 'Pre-seed,Seed',
            'preferred_industry': 'Agritech,E-commerce',
            'preferred_startup_age': '0-2',
            'preferred_business_model': 'Freemium,E-commerce',
            'min_investment': 2000,
            'max_investment': 50000,
        },
        {
            'investment_company': 'OPQ Investment Group',
            'investor_type': 'VC Fund',
            'preferred_country': 'Canada',
            'preferred_business_priority': 'User Acquisition,Brand Recognition',
            'preferred_founder_gender': 'Non-Binary',
            'preferred_investment_round': 'Series A,Series B',
            'preferred_industry': 'Biotech,Real Estate',
            'preferred_startup_age': '3-7',
            'preferred_business_model': 'Subscription,SaaS',
            'min_investment': 15000,
            'max_investment': 120000,
        }
    ]
    return dummy_data

def explore_page():
    st.title("Explore Investor Profiles 🌍")

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
    investor_profiles = fetch_all_investors()

    # Apply filters
    if investor_type_filter:
        investor_profiles = [profile for profile in investor_profiles if any(item in investor_type_filter for item in profile['investor_type'].split(','))]
    if country_filter:
        investor_profiles = [profile for profile in investor_profiles if any(item in country_filter for item in profile['preferred_country'].split(','))]
    if industry_filter:
        investor_profiles = [profile for profile in investor_profiles if any(item in industry_filter for item in profile['preferred_industry'].split(','))]
    if min_investment_filter:
        investor_profiles = [profile for profile in investor_profiles if profile['min_investment'] >= min_investment_filter]
    if max_investment_filter:
        investor_profiles = [profile for profile in investor_profiles if profile['max_investment'] <= max_investment_filter]

    # Convert list of dictionaries to DataFrame and display
    df = pd.DataFrame(investor_profiles)
    st.dataframe(df)

if __name__ == "__main__":
    explore_page()
