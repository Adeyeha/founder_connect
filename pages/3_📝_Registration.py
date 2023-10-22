import sys
sys.path.append(r'utils')
import streamlit as st
# Set page config
st.set_page_config(page_title="Founder's Connect Registration", page_icon="📝", layout="centered")

from streamlit_extras.switch_page_button import switch_page 
from utils import helpers,db
helpers.add_home_page()

def registration_page():

    # Page Heading
    st.title("Begin Your Journey with Founder's Connect 🚀")
    st.write("Take the first step towards connecting with the ideal startups or investors tailored for your needs.")

    with st.form("registration",clear_on_submit=True):
        username = st.text_input("Username", placeholder = "Johny001")

        col1, col2 = st.columns(2)
        
        first_name = col1.text_input("First Name", placeholder="John")
        last_name = col2.text_input("Last Name", placeholder="Doe")
        
        email = st.text_input("Email", placeholder="johndoe@example.com")
        
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')
        
        user_type = st.selectbox("I am a", ["Startup", "Investor"])
        
        checkbox_val = st.checkbox("I agree to the Terms and Conditions")

        errors = False

        if st.form_submit_button("Register"):
            if not first_name:
                st.error("Please enter your first name.")
                errors = True
            
            if not username:
                st.error("Please enter your username.")
                errors = True
            
            
            if not last_name:
                st.error("Please enter your last name.")
                errors = True

            if not email:
                st.error("Please enter an email address.")
                errors = True

            if not password:
                st.error("Please enter a password.")
                errors = True

            if password != confirm_password:
                st.error("Passwords do not match.")
                errors = True

            if not user_type:
                st.error("Please enter a user type.")
                errors = True

            if not checkbox_val:
                st.error("You must agree to the Terms and Conditions to register.")
                errors = True

            if not errors:
                # database insertion logic here
                create_user_response = db.create_user(username,first_name,last_name,user_type,email,password)
                if create_user_response:
                    st.error(f"Error during registration: {create_user_response}")
                else:
                    st.success(f"Welcome {first_name}! Registration successful. Let's embark on this exciting journey together.")
                    switch_page("Sign_In")
            
    col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

    sign_in = col4.button("Sign In")
    if sign_in:
        switch_page("Sign_In")


if __name__ == "__main__":
    registration_page()
