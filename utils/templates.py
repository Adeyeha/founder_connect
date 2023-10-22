from streamlit_extras.switch_page_button import switch_page 
import streamlit as st
import helpers
from db import get_startup_profile,get_investor_profile

def user_signed_in():
    # If successfully authenticated
    if st.session_state.get("authentication_status") and st.session_state.get("username"):
        authenticator = st.session_state.get("fhx")
        authenticator.logout('Logout', 'sidebar')
    else:
        switch_page("Sign_In")

def signin_redirect():
    if st.session_state.get("authentication_status"):
        authenticator = st.session_state.get("fhx")
        authenticator.logout('Logout', 'sidebar')
        if st.session_state.get("user_type").lower() == 'startup':
            helpers.add_startup_pages()
            # Function call to fetch the startup profile data for a particular user
            user_startup_profile_data = get_startup_profile()
            if user_startup_profile_data:
                switch_page('Explore_Investors') # switch to explore page
            switch_page('Startup_Profile')
        elif st.session_state.get("user_type").lower() == 'investor':
            helpers.add_investor_pages()
            user_investor_profile_data = get_investor_profile()
            if user_investor_profile_data:
                pass # switch to explore page
            switch_page('Investor_Profile')

def confirm_investor_user():
    if not st.session_state.get("user_type").lower() == 'investor':
        switch_page('Sign_In')

def confirm_startup_user():
    if not st.session_state.get("user_type").lower() == 'startup':
        switch_page('Sign_In')
