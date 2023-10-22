import sys
sys.path.append(r'utils')
import streamlit as st


# Set page configuration
st.set_page_config(
    page_title="Investors Details", 
    page_icon="📊", 
    layout="centered"
)

import db
from options import *
from templates import user_signed_in,confirm_startup_user
import helpers
import score
import plotly.express as px
# import plotly.graph_objects as go
import pandas as pd
# from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
from streamlit_extras.switch_page_button import switch_page 


helpers.add_startup_pages()

def investor_details_page():

    user_signed_in()
    confirm_startup_user()

    col1,col2 = st.columns([7,1])
    col1.title("Investor Details 💼")
    back = col2.button("Back") 
    if back:
        switch_page("Recommend_Investors")

    if st.session_state.get('selected_investor_metrics') and st.session_state.get('selected_investor_score') and st.session_state.get('selected_investor') and st.session_state.get('selected_investor_profile'):

        df = pd.DataFrame(list(st.session_state['selected_investor_metrics'].items()),columns=['theta','r'])
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        fig.update_traces(fill='toself')


        fig1 = go.Figure(go.Indicator(
            mode = "gauge+delta+number",
            value = int(st.session_state['selected_investor_score']),
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
            def display_investor_data(data):
                st.title(data['investment_company'])
                
                st.header("Investor Details:")
                st.write(f"**Investor Type:** {', '.join(data['investor_type'])}")
                st.write(f"**Description:** {data['investor_description']}")
                st.write(f"**Expertise:** {', '.join(data['investor_expertise'])}")
                
                st.header("Investment Preferences:")
                st.write(f"**Preferred Attributes:** {', '.join(data['preferred_attributes'])}")
                st.write(f"**Business Priority:** {', '.join(data['preferred_business_priority'])}")
                st.write(f"**Founder Gender Preference:** {', '.join(data['preferred_founder_gender'])}")
                st.write(f"**Investment Round Preference:** {', '.join(data['preferred_investment_round'])}")
                st.write(f"**Industry Preference:** {', '.join(data['preferred_industry'])}")
                st.write(f"**Country Preference:** {', '.join(data['preferred_country'])}")
                
                st.header("Investment Range:")
                st.write(f"**Minimum Investment:** ${data['min_investment']}")
                st.write(f"**Maximum Investment:** ${data['max_investment']}")
                
                st.header("Investment History:")
                st.write(f"**Past Investments:** ${data['past_investments']}")
                st.write(f"**Successful Exits:** {data['successful_exits']}")
                
                st.header("Startup Preferences:")
                st.write(f"**Preferred Startup Age:** {data['preferred_startup_age_min']} to {data['preferred_startup_age_max']} years")
                st.write(f"**Business Model Preference:** {', '.join(data['preferred_business_model'])}")
                st.write(f"**Business Stage Preference:** {', '.join(data['preferred_business_stage'])}")
                st.write(f"**Engagement Length Preference:** {', '.join(data['preferred_engagement_length'])}")
                st.write(f"**Engagement Model Preference:** {', '.join(data['preferred_engagement_model'])}")
                st.write(f"**Team Size Preference:** {data['preferred_team_size_min']} to {data['preferred_team_size_max']}")

            display_investor_data(st.session_state['selected_investor_profile'])


    else:
        switch_page('Recommend_Investors')


if __name__ == "__main__":
    investor_details_page()





