import sys
sys.path.append(r'utils')
import streamlit as st

# Set page config
st.set_page_config(page_title="Founder's Connect Sign In", page_icon="🔐", layout="centered")

import streamlit_authenticator as stauth
from streamlit_extras.switch_page_button import switch_page 
from templates import signin_redirect
from utils import helpers, db

# Cleanup 
helpers.add_home_page()

def signin_page():

    # Initial check for authentication
    if st.session_state.get("authentication_status") and st.session_state.get("username"):
        signin_redirect()
    else:
        config = db.get_users()

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            # config['preauthorized']
        )

        name, authentication_status, username = authenticator.login('Login', 'main')

        # If successfully authenticated
        if st.session_state.get("authentication_status"):
            user_dets = db.get_user(username)
            if user_dets is None:
                switch_page("Registration")
            username, user_type, email, first_name = user_dets
            st.session_state["user_type"] = user_type
            st.session_state["fhx"] = authenticator   
            signin_redirect()
        else:
            if st.session_state.get("authentication_status") is False:
                st.error('Username/password is incorrect')
            elif st.session_state.get("authentication_status") is None:
                st.warning('Please enter your username and password')
        
        col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

        register = col4.button("Register")
        if register:
            switch_page("Registration")

if __name__ == "__main__":
    signin_page()
