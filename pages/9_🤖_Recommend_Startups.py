import sys
sys.path.append(r'utils')
import streamlit as st


# Set page configuration
st.set_page_config(
    page_title="Recommend Startups", 
    page_icon="🤖", 
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
from streamlit_plotly_events import plotly_events
from streamlit_extras.switch_page_button import switch_page 


helpers.add_investor_pages()

def recommendation_page():

    user_signed_in()
    confirm_investor_user()

    st.title("Recommended Startup Profiles 🚀")

    # Fetch all investor profiles (or apply filters as needed)
    startup_profiles = db.get_startups()
    investor_profile = db.get_investor_profile()

    if investor_profile:

        # Filtering options
        st.sidebar.header("Filter Settings")
        top_n = st.sidebar.slider('Top N Records', 1, len(investor_profile), min(10, len(investor_profile)//2))
        orientation = st.sidebar.radio('Plot Orientation', ('Vertical', 'Horizontal'))  # New line for orientation selection

        # Generate scores
        scs = {}
        scs_w = {}
        for x in startup_profiles:
            scs[x['startup_company']], scs_w[x['startup_company']] = score.generate_scores(x, investor_profile, 'investor')

        # Sorting and filtering scores
        sorted_scores = sorted(scs_w.items(), key=lambda x: x[1], reverse=True)[:top_n]
        sorted_scores_df = pd.DataFrame(sorted_scores, columns=['Startup Company', 'Score'])



        def find_dict_by_key_value(lst, key, value):
            return next((d for d in lst if d.get(key) == value), None)

        # Plotting the scores using Plotly Express
        if orientation == 'Vertical':
            fig = px.bar(sorted_scores_df, 
                            x='Startup Company', 
                            y='Score', 
                            title='Startup Scores',
                            color_discrete_sequence=['#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf'],   
                            )
        else:
            # Sort the DataFrame in ascending order for horizontal orientation
            sorted_scores_df_1 = sorted_scores_df.sort_values(by='Score', ascending=True)
            fig = px.bar(sorted_scores_df_1, 
                            y='Startup Company', 
                            x='Score', 
                            orientation='h', 
                            title='Startup Scores',
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
                st.session_state['selected_startup'] = selected_points[0]['x']
                st.session_state['selected_startup_score'] = selected_points[0]['y']
                st.session_state['selected_startup_metrics'] = scs[selected_points[0]['x']]
                st.session_state['selected_startup_profile'] = find_dict_by_key_value(startup_profiles, 'startup_company', selected_points[0]['x'])
                switch_page('Startups_Details')
            else:
                st.session_state['selected_startup'] = selected_points[0]['y']
                st.session_state['selected_startup_score'] = selected_points[0]['x']
                st.session_state['selected_startup_metrics'] = scs[selected_points[0]['y']]
                st.session_state['selected_startup_profile'] = find_dict_by_key_value(startup_profiles, 'startup_company', selected_points[0]['y'])
                switch_page('Startups_Details')

    else:
        st.error("No Profile Found for Iinvestor. Create One in Profile then return to this page.")
        # redirect to profile

if __name__ == "__main__":
    recommendation_page()




