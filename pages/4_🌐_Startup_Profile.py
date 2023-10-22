import sys
sys.path.append(r'utils')
import streamlit as st

# change default values to placeholders
# check for all - reomve all

# Set page configuration
st.set_page_config(
    page_title="Startup's Profile", 
    page_icon="🚀", 
    layout="centered"
)

import db
from options import *
from templates import user_signed_in,confirm_startup_user
import helpers
helpers.add_startup_pages()

def startup_profile_page():

    user_signed_in()
    confirm_startup_user()

    st.title("Startup's Profile Page 🚀")
    st.write("Take your first step into finding potential Investors")

    user_startup_profile_data = db.get_startup_profile()

    with st.form("startup_profile_form", clear_on_submit=True):

        if not user_startup_profile_data:
            # Startup Details
            with st.container():
                st.subheader("Startup Details")
                startup_company = st.text_input("Startup Company", "e.g. MyStartup Inc.")
                startup_website = st.text_input("Startup Website", "e.g. https://mystartup.com")
                col1,col2 = st.columns(2)
                startup_stage = col1.selectbox("Startup Stage", STARTUP_STAGES)
                startup_industries = col2.multiselect("Startup Industry", INDUSTRIES)
                col1,col2 = st.columns([1,2])
                startup_countries = col1.selectbox("Startup Registration Country", COUNTRIES)
                startup_age = col2.slider("Startup  Age (yrs)", 0, 25)
                mission = st.text_area("Company's Mission", "Enter a brief mission statement...")
                long_term_goals = st.text_area("Long Term Goals", "What the startup aims to achieve in 5 years or more...")
                col1,col2 = st.columns(2)
                current_capital = col1.number_input("Current Capital", value=20000.0, step=1000.0)
                current_investment = col2.number_input("Current Investment", value=20000.0, step=1000.0)
                investment_needed = col1.number_input("Investment Needed", value=20000.0, step=1000.0)
                business_priorities = col2.multiselect("Business Priority", BUSINESS_PRIORITIES)

            # Founders Details
            with st.container():
                st.subheader("Founders Details")
                founder_name = st.text_input("Founder Name", "e.g. John Doe")
                founder_positions = st.multiselect("Founder other held positions", FOUNDER_POSITIONS)
                col1,col2 = st.columns([1,2])
                founder_gender = col1.selectbox("Founder Gender", GENDERS)
                team_size = col2.slider("Total Team Size", 1, 100)
                key_team_expertise = st.multiselect("Key Team Expertise", KEY_TEAM_EXPERTISE)

            # Product Details
            with st.container():
                st.subheader("Product Details")
                product_description = st.text_area("Product Description", "Brief about the product/service...")
                col1,col2 = st.columns(2)
                business_models = col1.multiselect("Business Model", BUSINESS_MODELS)
                product_stages = col2.selectbox("Product Stage", PRODUCT_STAGES)
                monthly_users = st.slider("Monthly Active Users", 0, 1000000)
            
            # Investor Engagement
            with st.container():
                st.subheader("Investor Engagement")
                col1,col2 = st.columns([2,1])
                investor_attributes = col1.multiselect("Which of these attributes does your startup possess?", PREFERRED_ATTRIBUTES)
                investment_round = col2.selectbox("Investment Round", INVESTMENT_ROUNDS)
                investor_expertise = st.multiselect("Sought Investor Expertise", INVESTOR_EXPERTISE)
                engagement_lengths = st.multiselect("Sought Engagement Length", ENGAGEMENT_LENGTHS)
                engagement_models = st.multiselect("Sought Engagement Model", ENGAGEMENT_MODELS)

            # Business Metrics
            with st.container():
                st.subheader("Business Metrics")
                revenue_models = st.multiselect("Revenue Model", REVENUE_MODELS)
                col1,col2 = st.columns(2)
                revenue = col1.number_input("Monthly/Annual Revenue", value=0.0)
                profit_margin = col2.number_input("Profit Margin", value=0.0,  max_value=1.0, min_value=0.0, step=0.1)
                churn_rate = st.slider("Churn Rate (%)", 0,100)

            # Intellectual Property and Market Position
            with st.container():
                st.subheader("Intellectual Property and Market Position")
                intellectual_properties = st.multiselect("Intellectual Property", INTELLECTUAL_PROPERTY)
                competitive_advantage = st.text_area("Competitive Advantage")
                current_challenges = st.text_area("Current Challenges")

        else:
            with st.container():
                st.subheader("Startup Details")
                startup_company = st.text_input("Startup Company", value=user_startup_profile_data.get('startup_company', "e.g. MyStartup Inc."))
                startup_website = st.text_input("Startup Website", value=user_startup_profile_data.get('startup_website', "e.g. https://mystartup.com"))
                col1, col2 = st.columns(2)
                startup_stage = col1.selectbox("Startup Stage", STARTUP_STAGES, index=STARTUP_STAGES.index(user_startup_profile_data.get('startup_stage', STARTUP_STAGES[0])))
                startup_industries = col2.multiselect("Startup Industry", INDUSTRIES, default=user_startup_profile_data.get('startup_industries', []))
                col1, col2 = st.columns([1, 2])
                startup_countries = col1.selectbox("Startup Registration Country", COUNTRIES, index=COUNTRIES.index(user_startup_profile_data.get('startup_countries', COUNTRIES[0])))
                startup_age = col2.slider("Startup Age (yrs)", 0, 25, value=user_startup_profile_data.get('startup_age', 0))
                mission = st.text_area("Company's Mission", value=user_startup_profile_data.get('mission', "Enter a brief mission statement..."))
                long_term_goals = st.text_area("Long Term Goals", value=user_startup_profile_data.get('long_term_goals', "What the startup aims to achieve in 5 years or more..."))
                col1, col2 = st.columns(2)
                current_capital = col1.number_input("Current Capital", value=user_startup_profile_data.get('current_capital', 20000.0), step=1000.0)
                current_investment = col2.number_input("Current Investment", value=user_startup_profile_data.get('current_investment', 20000.0), step=1000.0)
                investment_needed = col1.number_input("Investment Needed", value=user_startup_profile_data.get('investment_needed', 20000.0), step=1000.0)
                business_priorities = col2.multiselect("Business Priority", BUSINESS_PRIORITIES, default=user_startup_profile_data.get('business_priorities', []))

            # Founders Details
            with st.container():
                st.subheader("Founders Details")
                founder_name = st.text_input("Founder Name", value=user_startup_profile_data.get('founder_name', "e.g. John Doe"))
                founder_positions = st.multiselect("Founder other held positions", FOUNDER_POSITIONS, default=user_startup_profile_data.get('founder_positions', []))
                col1, col2 = st.columns([1, 2])
                founder_gender = col1.selectbox("Founder Gender", GENDERS, index=GENDERS.index(user_startup_profile_data.get('founder_gender', GENDERS[0])))
                team_size = col2.slider("Total Team Size", 1, 100, value=user_startup_profile_data.get('team_size', 1))
                key_team_expertise = st.multiselect("Key Team Expertise", KEY_TEAM_EXPERTISE, default=user_startup_profile_data.get('key_team_expertise', []))

            # Product Details
            with st.container():
                st.subheader("Product Details")
                product_description = st.text_area("Product Description", value=user_startup_profile_data.get('product_description', "Brief about the product/service..."))
                col1, col2 = st.columns(2)
                business_models = col1.multiselect("Business Model", BUSINESS_MODELS, default=user_startup_profile_data.get('business_models', []))
                product_stages = col2.selectbox("Product Stage", PRODUCT_STAGES, index=PRODUCT_STAGES.index(user_startup_profile_data.get('product_stages', PRODUCT_STAGES[0])))
                monthly_users = st.slider("Monthly Active Users", 0, 1000000, value=user_startup_profile_data.get('monthly_users', 0))

            # Investor Engagement
            with st.container():
                st.subheader("Investor Engagement")
                col1, col2 = st.columns([2, 1])
                investor_attributes = col1.multiselect("Which of these attributes does your startup possess?", PREFERRED_ATTRIBUTES, default=user_startup_profile_data.get('investor_attributes', []))
                investment_round = col2.selectbox("Investment Round", INVESTMENT_ROUNDS, index=INVESTMENT_ROUNDS.index(user_startup_profile_data.get('investment_round', INVESTMENT_ROUNDS[0])))
                investor_expertise = st.multiselect("Sought Investor Expertise", INVESTOR_EXPERTISE, default=user_startup_profile_data.get('investor_expertise', []))
                engagement_lengths = st.multiselect("Sought Engagement Length", ENGAGEMENT_LENGTHS, default=user_startup_profile_data.get('engagement_lengths', []))
                engagement_models = st.multiselect("Sought Engagement Model", ENGAGEMENT_MODELS, default=user_startup_profile_data.get('engagement_models', []))

            # Business Metrics
            with st.container():
                st.subheader("Business Metrics")
                revenue_models = st.multiselect("Revenue Model", REVENUE_MODELS, default=user_startup_profile_data.get('revenue_models', []))
                col1, col2 = st.columns(2)
                revenue = col1.number_input("Monthly/Annual Revenue", value=user_startup_profile_data.get('revenue', 0.0))
                profit_margin = col2.number_input("Profit Margin", value=user_startup_profile_data.get('profit_margin', 0.0),  max_value=1.0, min_value=0.0, step=0.1)
                churn_rate = st.slider("Churn Rate (%)", 0, 100, value=int(user_startup_profile_data.get('churn_rate', 0)))

            # Intellectual Property and Market Position
            with st.container():
                st.subheader("Intellectual Property and Market Position")
                intellectual_properties = st.multiselect("Intellectual Property", INTELLECTUAL_PROPERTY, default=user_startup_profile_data.get('intellectual_properties', []))
                competitive_advantage = st.text_area("Competitive Advantage", value=user_startup_profile_data.get('competitive_advantage', ""))
                current_challenges = st.text_area("Current Challenges", value=user_startup_profile_data.get('current_challenges', ""))

        errors = False
        if st.form_submit_button("Save"):

            if not startup_company:
                st.error("Startup Company field is required.")
                errors = True

            if not startup_website:
                st.error("Startup Website field is required.")
                errors = True
            
            if not startup_stage:
                st.error("Startup Stage field is required.")
                errors = True

            if not startup_industries:
                st.error("Startup Industry field is required.")
                errors = True

            if not startup_countries:
                st.error("Startup Registration Country field is required.")
                errors = True

            if not mission:
                st.error("Company's Mission field is required.")
                errors = True

            if not long_term_goals:
                st.error("Long Term Goals field is required.")
                errors = True

            if not founder_name:
                st.error("Founder Name field is required.")
                errors = True

            if not key_team_expertise:
                st.error("Key Team Expertise field is required.")
                errors = True

            if not product_description:
                st.error("Product Description field is required.")
                errors = True

            if not business_models:
                st.error("Business Model field is required.")
                errors = True

            if not investor_attributes:
                st.error("Investor Attributes field is required.")
                errors = True

            if not investor_expertise:
                st.error("Sought Investor Expertise field is required.")
                errors = True

            if not revenue_models:
                st.error("Revenue Model field is required.")
                errors = True

            if not intellectual_properties:
                st.error("Intellectual Property field is required.")
                errors = True

            if not competitive_advantage:
                st.error("Competitive Advantage field is required.")
                errors = True

            if not current_challenges:
                st.error("Current Challenges field is required.")
                errors = True

            # Startup Details Section
            if startup_age is None:
                st.error("Startup Age field is required.")
                errors = True

            if not current_capital:
                st.error("Current Capital field is required.")
                errors = True

            if not current_investment:
                st.error("Current Investment field is required.")
                errors = True

            if not investment_needed:
                st.error("Investment Needed field is required.")
                errors = True

            if not business_priorities:
                st.error("Business Priority field is required.")
                errors = True

            # Founders Details Section
            if not founder_positions:
                st.error("Founder other held positions field is required.")
                errors = True

            if not founder_gender:
                st.error("Founder Gender field is required.")
                errors = True

            if not team_size:
                st.error("Total Team Size field is required.")
                errors = True

            # Product Details Section
            if not product_stages:
                st.error("Product Stage field is required.")
                errors = True

            if monthly_users is None:
                st.error("Monthly Active Users field is required.")
                errors = True

            # Investor Engagement Section
            if not investment_round:
                st.error("Investment Round field is required.")
                errors = True

            if not engagement_lengths:
                st.error("Sought Engagement Length field is required.")
                errors = True

            if not engagement_models:
                st.error("Sought Engagement Model field is required.")
                errors = True

            # Business Metrics Section
            if revenue is None:
                st.error("Monthly/Annual Revenue field is required.")
                errors = True

            if profit_margin is None:
                st.error("Profit Margin field is required.")
                errors = True

            if churn_rate is None:
                st.error("Churn Rate (%) field is required.")
                errors = True

            # Logic for saving or processing the form data
            if not errors:
                        # If no errors, proceed with database insertion
                        create_response = db.create_startup_profile(
                            startup_company, startup_website, startup_stage, startup_industries,
                            startup_countries, startup_age, mission, long_term_goals,
                            current_capital, current_investment, investment_needed, business_priorities,
                            founder_name, founder_positions, founder_gender, team_size,
                            key_team_expertise, product_description, business_models, product_stages,
                            monthly_users, investor_attributes, investment_round, investor_expertise,
                            engagement_lengths, engagement_models, revenue_models, revenue,
                            profit_margin, churn_rate, intellectual_properties, competitive_advantage,
                            current_challenges
                        )

                        if create_response:  # Assuming create_response returns an error message if something goes wrong
                            st.error(f"Error during profile creation: {create_response}")
                        else:
                            st.success(f"Profile for {startup_company} created successfully.")

if __name__ == "__main__":
    startup_profile_page()
