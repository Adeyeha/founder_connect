import sys
sys.path.append(r'utils')
import streamlit as st

# Set page configurations
st.set_page_config(page_title="Founder's Connect", page_icon="🚀", layout="centered")

import helpers
from streamlit_extras.switch_page_button import switch_page 

# from utils.dummy_data import investor_data_variations
from utils.db import sample_investors,sample_startups


# Delete all pages
helpers.add_home_page()

def landing_page():
    # Logo (Replace 'logo.png' with the path to your logo)
    # st.image('logo.png', width=200)

    # Page Heading
    st.title("Welcome to Founder's Connect 🚀")
    st.write("Connecting Startups with the Perfect Investors!")

    st.write("""
    **Founder's Connect** is the premier platform where startups meet their ideal investors.
    Dive into a world of opportunities and let us find the perfect match for your entrepreneurial journey.
    Your dreams deserve the right backing. Start now!
    """)

    col1,col2,col3,col4,col5,col6 = st.columns(6)
    sign_in = col2.button("Sign In")
    if sign_in:
        switch_page("Sign_In")

    register = col5.button("Register")
    if register:
        switch_page("Registration")

if __name__ == "__main__":
    landing_page()
