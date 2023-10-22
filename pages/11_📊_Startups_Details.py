import sys
sys.path.append(r'utils')
import streamlit as st


# Set page configuration
st.set_page_config(
    page_title="Startup Details", 
    page_icon="📊", 
    layout="centered"
)

import db
from options import *
from templates import user_signed_in,confirm_investor_user
import helpers
import score
import plotly.express as px
# import plotly.graph_objects as go
import pandas as pd
# from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page 


helpers.add_investor_pages()

def startup_details_page():

    user_signed_in()
    confirm_investor_user()

    col1,col2 = st.columns([7,1])
    col1.title("Startup Details 🚀")
    back = col2.button("Back") 
    if back:
        switch_page("Recommend_Startups")

    if st.session_state.get('selected_startup_metrics') and st.session_state.get('selected_startup_score') and st.session_state.get('selected_startup') and st.session_state.get('selected_startup_profile'):

        df = pd.DataFrame(list(st.session_state['selected_startup_metrics'].items()),columns=['theta','r'])
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')


        fig1 = go.Figure(go.Indicator(
            mode = "gauge+delta+number",
            value = int(st.session_state['selected_startup_score']),
            delta = {'reference': 100},
            gauge = {
                'shape': "bullet",
                'axis': {'visible': True, 'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#377eb8"},
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 250
                }
            },
            domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
            ))


        tab1, tab2 = st.tabs(["Analytics", "Details"])
        with tab1:
            with st.container():
                st.subheader('Similarity Guage')
                st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
            with st.container():
                st.subheader('Radar Chart')
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        with tab2:
            def display_startup_data(data):
                st.title(data['startup_company'])
                
                st.header("Startup Details:")
                st.write(f"**Website:** {data['startup_website']}")
                st.write(f"**Stage:** {data['startup_stage']}")
                st.write(f"**Industries:** {', '.join(data['startup_industries'])}")
                st.write(f"**Countries:** {data['startup_countries']}")
                st.write(f"**Age:** {data['startup_age']} years")
                st.write(f"**Mission:** {data['mission']}")
                st.write(f"**Long-term Goals:** {data['long_term_goals']}")
                
                st.header("Financial Details:")
                st.write(f"**Current Capital:** ${data['current_capital']}")
                st.write(f"**Current Investment:** ${data['current_investment']}")
                st.write(f"**Investment Needed:** ${data['investment_needed']}")
                
                st.header("Team Details:")
                st.write(f"**Founder Name:** {data['founder_name']}")
                st.write(f"**Founder Positions:** {', '.join(data['founder_positions'])}")
                st.write(f"**Founder Gender:** {data['founder_gender']}")
                st.write(f"**Team Size:** {data['team_size']}")
                st.write(f"**Key Team Expertise:** {', '.join(data['key_team_expertise'])}")
                
                st.header("Product and Business Model:")
                st.write(f"**Product Description:** {data['product_description']}")
                st.write(f"**Business Models:** {', '.join(data['business_models'])}")
                st.write(f"**Product Stages:** {data['product_stages']}")
                
                st.header("User and Revenue Metrics:")
                st.write(f"**Monthly Users:** {data['monthly_users']}")
                st.write(f"**Revenue Models:** {', '.join(data['revenue_models'])}")
                st.write(f"**Revenue:** ${data['revenue']}")
                st.write(f"**Profit Margin:** {data['profit_margin'] * 100}%")
                st.write(f"**Churn Rate:** {data['churn_rate']}%")
                
                st.header("Investor Engagement:")
                st.write(f"**Investor Attributes:** {', '.join(data['investor_attributes'])}")
                st.write(f"**Investment Round:** {data['investment_round']}")
                st.write(f"**Investor Expertise:** {', '.join(data['investor_expertise'])}")
                st.write(f"**Engagement Lengths:** {', '.join(data['engagement_lengths'])}")
                st.write(f"**Engagement Models:** {', '.join(data['engagement_models'])}")
                
                st.header("Intellectual Properties and Competitive Advantages:")
                st.write(f"**Intellectual Properties:** {', '.join(data['intellectual_properties'])}")
                st.write(f"**Competitive Advantage:** {data['competitive_advantage']}")
                st.write(f"**Current Challenges:** {data['current_challenges']}")

            display_startup_data(st.session_state['selected_startup_profile'])

    else:
        switch_page('Recommend_Startups')


if __name__ == "__main__":
    startup_details_page()





