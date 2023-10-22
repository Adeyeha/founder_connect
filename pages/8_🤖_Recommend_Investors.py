import sys
sys.path.append(r'utils')
import streamlit as st


# Set page configuration
st.set_page_config(
    page_title="Recommend Investors", 
    page_icon="🤖", 
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
from streamlit_plotly_events import plotly_events
from streamlit_extras.switch_page_button import switch_page 


helpers.add_startup_pages()

def recommendation_page():

    user_signed_in()
    confirm_startup_user()

    st.title("Recommended Investor Profiles 💼")

    # Fetch all investor profiles (or apply filters as needed)
    investor_profiles = db.get_investors()
    startup_profile = db.get_startup_profile()

    if startup_profile:

        # Filtering options
        st.sidebar.header("Filter Settings")
        top_n = st.sidebar.slider('Top N Records', 1, len(investor_profiles), min(10, len(investor_profiles)//2))
        orientation = st.sidebar.radio('Plot Orientation', ('Vertical', 'Horizontal'))  # New line for orientation selection

        # Generate scores
        scs = {}
        scs_w = {}
        for x in investor_profiles:
            scs[x['investment_company']], scs_w[x['investment_company']] = score.generate_scores(x, startup_profile, 'startup')

        # Sorting and filtering scores
        sorted_scores = sorted(scs_w.items(), key=lambda x: x[1], reverse=True)[:top_n]
        sorted_scores_df = pd.DataFrame(sorted_scores, columns=['Investment Company', 'Score'])



        def find_dict_by_key_value(lst, key, value):
            return next((d for d in lst if d.get(key) == value), None)

        # Plotting the scores using Plotly Express
        if orientation == 'Vertical':
            fig = px.bar(sorted_scores_df, 
                            x='Investment Company', 
                            y='Score', 
                            title='Investor Scores',
                            color_discrete_sequence=['#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf'],   
                            )
        else:
            # Sort the DataFrame in ascending order for horizontal orientation
            sorted_scores_df_1 = sorted_scores_df.sort_values(by='Score', ascending=True)
            fig = px.bar(sorted_scores_df_1, 
                            y='Investment Company', 
                            x='Score', 
                            orientation='h', 
                            title='Investor Scores',
                            color_discrete_sequence=['#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf'],   
                            )  # Swap x and y for horizontal orientation

         # Adding a click event to the Plotly chart
        fig.update_layout(
            clickmode='event+select'
        )

        # Displaying the Plotly chart
        selected_points = plotly_events(fig)
        

        # Capturing the click event to get the selected company
        if len(selected_points)> 0:
            if orientation == 'Vertical':
                st.session_state['selected_investor'] = selected_points[0]['x']
                st.session_state['selected_investor_score'] = selected_points[0]['y']
                st.session_state['selected_investor_metrics'] = scs[selected_points[0]['x']]
                st.session_state['selected_investor_profile'] = find_dict_by_key_value(investor_profiles, 'investment_company', selected_points[0]['x'])
                switch_page('Investors_Details')
            else:
                st.session_state['selected_investor'] = selected_points[0]['y']
                st.session_state['selected_investor_score'] = selected_points[0]['x']
                st.session_state['selected_investor_metrics'] = scs[selected_points[0]['y']]
                st.session_state['selected_investor_profile'] = find_dict_by_key_value(investor_profiles, 'investment_company', selected_points[0]['y'])
                switch_page('Investors_Details')

    else:
        st.error("No Profile Found for Startup. Create One in Profile then return to this page.")
        # redirect to profile

if __name__ == "__main__":
    recommendation_page()




