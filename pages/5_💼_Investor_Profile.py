import sys
sys.path.append(r'utils')

import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Investor's Profile", 
    page_icon="💼", 
    layout="centered"
)

# Pass User iD
# clear form
# change default values to placeholders
# check usertype

# SHOW INVESTOR PAGES
import db
from options import *
from templates import user_signed_in, confirm_investor_user
import helpers
helpers.add_investor_pages()

def investor_profile_page():

    user_signed_in()
    confirm_investor_user()

    st.title("Investor's Profile Page 💼")
    st.write("Take your first step into finding potential Startups")

    user_investor_profile_data = db.get_investor_profile()

    with st.form("investor_profile_form",clear_on_submit=True):

        if not user_investor_profile_data:

            # Investor Details
            with st.container():
                st.subheader("Investor Details")
                investment_company = st.text_input("Investment Company", "e.g. ABC Investments Inc.")
                investor_type = st.multiselect("Investor Type", INVESTOR_TYPES)
                investor_description = st.text_area("Investor Description", "Describe the investor or the investment firm...")
                investor_expertise = st.multiselect("Investor Expertise", INVESTOR_EXPERTISE)
                
            # Preferences
            with st.container():
                st.subheader("Preferences")
                preferred_attributes = st.multiselect("Preferred Startup Attributes", PREFERRED_ATTRIBUTES)
                preferred_business_priority = st.multiselect("Preferred Business Priority", BUSINESS_PRIORITIES)
                preferred_founder_gender = st.multiselect("Preferred Founder Gender", GENDERS)
                preferred_investment_round = st.multiselect("Preferred Investment Round", INVESTMENT_ROUNDS)
                preferred_industry = st.multiselect("Preferred Industry", INDUSTRIES)
                preferred_country = st.multiselect("Preferred Country(s)", COUNTRIES)
                col1,col2 = st.columns(2)
                min_investment = col1.number_input("Min Investment", value=20000.0, step=1000.0)
                max_investment = col2.number_input("Max Investment", value=20000.0, step=1000.0)
                past_investments = col1.number_input("Past Investments", value=1000000.0, step=1000.0)
                successful_exits = col2.number_input("Successful Exits", value=10, step=1)
                preferred_startup_age = st.slider("Preferred Startup Age - yrs (Range)", 0, 50, (2, 10)) # Assuming a range from 0-20 years
                preferred_business_model = st.multiselect("Preferred Business Model", BUSINESS_MODELS)
                preferred_business_stage = st.multiselect("Preferred Business Stage", PRODUCT_STAGES)
                preferred_engagement_length = st.multiselect("Preferred Engagement Length", ENGAGEMENT_LENGTHS)
                preferred_engagement_model = st.multiselect("Preferred Engagement Model", ENGAGEMENT_MODELS)
                preferred_team_size = st.slider("Preferred Team Size (Range)", 0, 50, (2, 10))

        else:
            
            # Investor Details
            with st.container():
                st.subheader("Investor Details")
                investment_company = st.text_input("Investment Company", value=user_investor_profile_data.get('investment_company', "e.g. ABC Investments Inc."))
                investor_type = st.multiselect("Investor Type", INVESTOR_TYPES, default=user_investor_profile_data.get('investor_type', []))
                investor_description = st.text_area("Investor Description", value=user_investor_profile_data.get('investor_description', "Describe the investor or the investment firm..."))
                investor_expertise = st.multiselect("Investor Expertise", INVESTOR_EXPERTISE, default=user_investor_profile_data.get('investor_expertise', []))
                
            # Preferences
            with st.container():
                st.subheader("Preferences")
                preferred_attributes = st.multiselect("Preferred Startup Attributes", PREFERRED_ATTRIBUTES, default=user_investor_profile_data.get('preferred_attributes', []))
                preferred_business_priority = st.multiselect("Preferred Business Priority", BUSINESS_PRIORITIES, default=user_investor_profile_data.get('preferred_business_priority', []))
                preferred_founder_gender = st.multiselect("Preferred Founder Gender", GENDERS, default=user_investor_profile_data.get('preferred_founder_gender', []))
                preferred_investment_round = st.multiselect("Preferred Investment Round", INVESTMENT_ROUNDS, default=user_investor_profile_data.get('preferred_investment_round', []))
                preferred_industry = st.multiselect("Preferred Industry", INDUSTRIES, default=user_investor_profile_data.get('preferred_industry', []))
                preferred_country = st.multiselect("Preferred Country(s)", COUNTRIES, default=user_investor_profile_data.get('preferred_country', []))
                col1, col2 = st.columns(2)
                min_investment = col1.number_input("Min Investment", value=user_investor_profile_data.get('min_investment', 20000.0), step=1000.0)
                max_investment = col2.number_input("Max Investment", value=user_investor_profile_data.get('max_investment', 20000.0), step=1000.0)
                past_investments = col1.number_input("Past Investments", value=user_investor_profile_data.get('past_investments', 1000000.0), step=1000.0)
                successful_exits = col2.number_input("Successful Exits", value=user_investor_profile_data.get('successful_exits', 10), step=1)
                preferred_startup_age_min, preferred_startup_age_max = user_investor_profile_data.get('preferred_startup_age', (2, 10))  # Assuming a range from 0-50 years
                preferred_startup_age = st.slider("Preferred Startup Age - yrs (Range)", 0, 50, (preferred_startup_age_min, preferred_startup_age_max))
                preferred_business_model = st.multiselect("Preferred Business Model", BUSINESS_MODELS, default=user_investor_profile_data.get('preferred_business_model', []))
                preferred_business_stage = st.multiselect("Preferred Business Stage", PRODUCT_STAGES, default=user_investor_profile_data.get('preferred_business_stage', []))
                preferred_engagement_length = st.multiselect("Preferred Engagement Length", ENGAGEMENT_LENGTHS, default=user_investor_profile_data.get('preferred_engagement_length', []))
                preferred_engagement_model = st.multiselect("Preferred Engagement Model", ENGAGEMENT_MODELS, default=user_investor_profile_data.get('preferred_engagement_model', []))
                preferred_team_size_min, preferred_team_size_max = user_investor_profile_data.get('preferred_team_size', (2, 10))
                preferred_team_size = st.slider("Preferred Team Size (Range)", 0, 50, (preferred_team_size_min, preferred_team_size_max))

        errors = False  # Initialize errors flag

        if st.form_submit_button("Submit"):
            if not investment_company:
                st.error("Investment Company field is required.")
                errors = True

            if not investor_type:
                st.error("Investor Type field is required.")
                errors = True

            if not investor_description:
                st.error("Investor Description field is required.")
                errors = True

            if not investor_expertise:
                st.error("Investor Expertise field is required.")
                errors = True

            if not preferred_attributes:
                st.error("Preferred Startup Attributes field is required.")
                errors = True

            if not preferred_business_priority:
                st.error("Preferred Business Priority field is required.")
                errors = True

            if not preferred_founder_gender:
                st.error("Preferred Founder Gender field is required.")
                errors = True

            if not preferred_investment_round:
                st.error("Preferred Investment Round field is required.")
                errors = True

            if not preferred_industry:
                st.error("Preferred Industry field is required.")
                errors = True

            if not preferred_country:
                st.error("Preferred Country(s) field is required.")
                errors = True

            if not preferred_business_model:
                st.error("Preferred Business Model field is required.")
                errors = True

            if not preferred_business_stage:
                st.error("Preferred Business Stage field is required.")
                errors = True

            if not preferred_engagement_length:
                st.error("Preferred Engagement Length field is required.")
                errors = True

            if not preferred_engagement_model:
                st.error("Preferred Engagement Model field is required.")
                errors = True

            if not errors:
                # If no errors, proceed with database insertion
                create_response = db.create_investor_profile(
                    investment_company, investor_type, investor_description, investor_expertise, 
                    preferred_attributes, preferred_business_priority, preferred_founder_gender, 
                    preferred_investment_round, preferred_industry, preferred_country, 
                    min_investment, max_investment, past_investments, successful_exits, 
                    preferred_startup_age, preferred_business_model, preferred_business_stage, 
                    preferred_engagement_length, preferred_engagement_model, preferred_team_size
                )

                if create_response:  # Assuming create_response returns an error message if something goes wrong
                    st.error(f"Error during profile creation: {create_response}")
                else:
                    st.success(f"Profile for {investment_company} created successfully.")

        
if __name__ == "__main__":
    investor_profile_page()
