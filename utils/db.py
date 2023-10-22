from logging import raiseExceptions
import streamlit as st
import streamlit_authenticator as stauth
import string
import random
from options import *
 

# Create the SQL connection to founders_db.
conn = st.experimental_connection('founders_db', type='sql')

def create_user(username, first_name, last_name, user_type, email, password):
    try:
        # Table creation
        with conn.session as s:
            s.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    user_type TEXT,
                    email TEXT ,
                    password TEXT
                );
            ''')

            # Check for existing user
            existing_user = s.execute('SELECT * FROM users WHERE username = :username', 
                                      params=dict(username=username)).fetchall()

            if len(existing_user) > 0:
                return 'Username already exists'

            # Hash password
            password = stauth.Hasher([password]).generate()[0]
            # Insert new user
            s.execute('''
                INSERT INTO users (username, first_name, last_name, user_type, email, password)
                VALUES (:username, :first_name, :last_name, :user_type, :email, :password);
            ''', params=dict(username=username,first_name=first_name, last_name=last_name, user_type=user_type, email=email, password=password))

            s.commit()

            return None

    except Exception as e:
        return str(e)

def get_users():
    with conn.session as s:
        results = s.execute('SELECT username, password, user_type, email, first_name FROM users;').fetchall()
        
        credentials = {}
        for row in results:
            username, password, user_type, email, first_name = row
            credentials[username] = {
                'email': email,
                'name': first_name,
                'password': password,
                'user_type': user_type
            }
        
        return {
            'credentials': {'usernames': credentials},
            'cookie': {
                'expiry_days': 30,
                'key': 'random_signature_key',
                'name': 'xfh'
            },
            'preauthorized': {'emails': []}
        }

def get_user(username):
    with conn.session as s:
        results = s.execute('SELECT username, user_type, email, first_name FROM users where username = :username;', params=dict(username=username)).fetchone()
        
        if results is not None:
            username, user_type, email, first_name = results
            return username, user_type, email, first_name
        
    return None
    

def create_investor_profile(investment_company, investor_type, investor_description, investor_expertise, 
                            preferred_attributes, preferred_business_priority, preferred_founder_gender, 
                            preferred_investment_round, preferred_industry, preferred_country, 
                            min_investment, max_investment, past_investments, successful_exits, 
                            preferred_startup_age, preferred_business_model, preferred_business_stage, 
                            preferred_engagement_length, preferred_engagement_model, preferred_team_size):
    try:
        # Assuming you have an established database connection named 'conn'
        with conn.session as s:
            # Table creation for investor profiles
            s.execute('''
                CREATE TABLE IF NOT EXISTS investor_profiles (
                    investment_company TEXT,
                    investor_type TEXT,
                    investor_description TEXT,
                    investor_expertise TEXT,
                    preferred_attributes TEXT,
                    preferred_business_priority TEXT,
                    preferred_founder_gender TEXT,
                    preferred_investment_round TEXT,
                    preferred_industry TEXT,
                    preferred_country TEXT,
                    min_investment REAL,
                    max_investment REAL,
                    past_investments REAL,
                    successful_exits INTEGER,
                    preferred_startup_age_min  INTEGER,
                    preferred_startup_age_max INTEGER,
                    preferred_business_model TEXT,
                    preferred_business_stage TEXT,
                    preferred_engagement_length TEXT,
                    preferred_engagement_model TEXT,
                    preferred_team_size_min INTEGER,
                    preferred_team_size_max INTEGER,
                    user TEXT PRIMARY KEY
                );
            ''')

            # Delete existing investor record
            s.execute('delete from investor_profiles where user = :user;',{'user': st.session_state.get('username')})

            # Inserting new investor profile
            s.execute('''
                INSERT INTO investor_profiles (
                    investment_company, investor_type, investor_description, investor_expertise, preferred_attributes,
                    preferred_business_priority, preferred_founder_gender, preferred_investment_round, preferred_industry,
                    preferred_country, min_investment, max_investment, past_investments, successful_exits, 
                    preferred_startup_age_min, preferred_startup_age_max, preferred_business_model, preferred_business_stage, 
                    preferred_engagement_length, preferred_engagement_model, preferred_team_size_min, preferred_team_size_max, user
                ) VALUES (
                    :investment_company, :investor_type, :investor_description, :investor_expertise, :preferred_attributes,
                    :preferred_business_priority, :preferred_founder_gender, :preferred_investment_round, :preferred_industry,
                    :preferred_country, :min_investment, :max_investment, :past_investments, :successful_exits, 
                    :preferred_startup_age_min, :preferred_startup_age_max, :preferred_business_model, :preferred_business_stage, 
                    :preferred_engagement_length, :preferred_engagement_model, :preferred_team_size_min, :preferred_team_size_max, :user
                );
            ''', {
                    'investment_company': investment_company,
                    'investor_type': ','.join(investor_type),
                    'investor_description': investor_description,
                    'investor_expertise': ','.join(investor_expertise),
                    'preferred_attributes': ','.join(preferred_attributes),
                    'preferred_business_priority': ','.join(preferred_business_priority),
                    'preferred_founder_gender': ','.join(preferred_founder_gender),
                    'preferred_investment_round': ','.join(preferred_investment_round),
                    'preferred_industry': ','.join(preferred_industry),
                    'preferred_country': ','.join(preferred_country),
                    'min_investment': min_investment,
                    'max_investment': max_investment,
                    'past_investments': past_investments,
                    'successful_exits': successful_exits,
                    'preferred_startup_age_min': preferred_startup_age[0],
                    'preferred_startup_age_max': preferred_startup_age[1],
                    'preferred_business_model': ','.join(preferred_business_model),
                    'preferred_business_stage': ','.join(preferred_business_stage),
                    'preferred_engagement_length': ','.join(preferred_engagement_length),
                    'preferred_engagement_model': ','.join(preferred_engagement_model),
                    'preferred_team_size_min': preferred_team_size[0],
                    'preferred_team_size_max': preferred_team_size[1],
                    'user': st.session_state.get('username')
                })

            s.commit()

    except Exception as e:
        return str(e)  # Return the error message

    return None  # Return None if everything is successful



def create_startup_profile(
    startup_company, startup_website, startup_stage, startup_industries,
    startup_countries, startup_age, mission, long_term_goals,
    current_capital, current_investment, investment_needed, business_priorities,
    founder_name, founder_positions, founder_gender, team_size,
    key_team_expertise, product_description, business_models, product_stages,
    monthly_users, investor_attributes, investment_round, investor_expertise,
    engagement_lengths, engagement_models, revenue_models, revenue,
    profit_margin, churn_rate, intellectual_properties, competitive_advantage,
    current_challenges
):
    try:
        # Assuming you have an established database connection named 'conn'
        with conn.session as s:
            # Table creation for startup profiles
            s.execute('''
                CREATE TABLE IF NOT EXISTS startup_profiles (
                    startup_company TEXT,
                    startup_website TEXT,
                    startup_stage TEXT,
                    startup_industries TEXT,
                    startup_countries TEXT,
                    startup_age INTEGER,
                    mission TEXT,
                    long_term_goals TEXT,
                    current_capital REAL,
                    current_investment REAL,
                    investment_needed REAL,
                    business_priorities TEXT,
                    founder_name TEXT,
                    founder_positions TEXT,
                    founder_gender TEXT,
                    team_size INTEGER,
                    key_team_expertise TEXT,
                    product_description TEXT,
                    business_models TEXT,
                    product_stages TEXT,
                    monthly_users INTEGER,
                    investor_attributes TEXT,
                    investment_round TEXT,
                    investor_expertise TEXT,
                    engagement_lengths TEXT,
                    engagement_models TEXT,
                    revenue_models TEXT,
                    revenue REAL,
                    profit_margin REAL,
                    churn_rate REAL,
                    intellectual_properties TEXT,
                    competitive_advantage TEXT,
                    current_challenges TEXT,
                    user TEXT PRIMARY KEY
                );
            ''')

            # Delete existing startup record
            s.execute('delete from startup_profiles where user = :user;',{'user': st.session_state.get('username')})

            # Inserting new startup profile
            s.execute('''
                INSERT INTO startup_profiles (
                    startup_company, startup_website, startup_stage, startup_industries, startup_countries,
                    startup_age, mission, long_term_goals, current_capital, current_investment,
                    investment_needed, business_priorities, founder_name, founder_positions, founder_gender,
                    team_size, key_team_expertise, product_description, business_models, product_stages,
                    monthly_users, investor_attributes, investment_round, investor_expertise,
                    engagement_lengths, engagement_models, revenue_models, revenue,
                    profit_margin, churn_rate, intellectual_properties, competitive_advantage,
                    current_challenges,user
                ) VALUES (
                    :startup_company, :startup_website, :startup_stage, :startup_industries, :startup_countries,
                    :startup_age, :mission, :long_term_goals, :current_capital, :current_investment,
                    :investment_needed, :business_priorities, :founder_name, :founder_positions, :founder_gender,
                    :team_size, :key_team_expertise, :product_description, :business_models, :product_stages,
                    :monthly_users, :investor_attributes, :investment_round, :investor_expertise,
                    :engagement_lengths, :engagement_models, :revenue_models, :revenue,
                    :profit_margin, :churn_rate, :intellectual_properties, :competitive_advantage,
                    :current_challenges,:user
                );
            ''', {
                    'startup_company': startup_company,
                    'startup_website': startup_website,
                    'startup_stage': startup_stage,
                    'startup_industries': ','.join(startup_industries),
                    'startup_countries': startup_countries,
                    'startup_age': startup_age,
                    'mission': mission,
                    'long_term_goals': long_term_goals,
                    'current_capital': current_capital,
                    'current_investment': current_investment,
                    'investment_needed': investment_needed,
                    'business_priorities': ','.join(business_priorities),
                    'founder_name': founder_name,
                    'founder_positions': ','.join(founder_positions),
                    'founder_gender': founder_gender,
                    'team_size': team_size,
                    'key_team_expertise': ','.join(key_team_expertise),
                    'product_description': product_description,
                    'business_models': ','.join(business_models),
                    'product_stages': product_stages,
                    'monthly_users': monthly_users,
                    'investor_attributes': ','.join(investor_attributes),
                    'investment_round': investment_round,
                    'investor_expertise': ','.join(investor_expertise),
                    'engagement_lengths': ','.join(engagement_lengths),
                    'engagement_models': ','.join(engagement_models),
                    'revenue_models': ','.join(revenue_models),
                    'revenue': revenue,
                    'profit_margin': profit_margin,
                    'churn_rate': churn_rate,
                    'intellectual_properties': ','.join(intellectual_properties),
                    'competitive_advantage': competitive_advantage,
                    'current_challenges': current_challenges,
                    'user': st.session_state.get('username')
                })

            s.commit()

    except Exception as e:
        return str(e)  # Return the error message

    return None  # Return None if everything is successful


def get_startup_profile():
    try:
        # Assuming you have an established database connection named 'conn'
        with conn.session as s:
            # Query to fetch the startup profile of a particular user
            result = s.execute('''
                SELECT * FROM startup_profiles WHERE user = :user;
            ''', {'user': st.session_state.get('username')})

            # Fetching the first (and presumably only) record that matches the user
            record = result.fetchone()

            if record:
                # Constructing a dictionary to hold the startup profile data
                startup_profile_data = {
                    'startup_company': record['startup_company'],
                    'startup_website': record['startup_website'],
                    'startup_stage': record['startup_stage'],
                    'startup_industries': record['startup_industries'].split(','),
                    'startup_countries': record['startup_countries'],
                    'startup_age': record['startup_age'],
                    'mission': record['mission'],
                    'long_term_goals': record['long_term_goals'],
                    'current_capital': record['current_capital'],
                    'current_investment': record['current_investment'],
                    'investment_needed': record['investment_needed'],
                    'business_priorities': record['business_priorities'].split(','),
                    'founder_name': record['founder_name'],
                    'founder_positions': record['founder_positions'].split(','),
                    'founder_gender': record['founder_gender'],
                    'team_size': record['team_size'],
                    'key_team_expertise': record['key_team_expertise'].split(','),
                    'product_description': record['product_description'],
                    'business_models': record['business_models'].split(','),
                    'product_stages': record['product_stages'],
                    'monthly_users': record['monthly_users'],
                    'investor_attributes': record['investor_attributes'].split(','),
                    'investment_round': record['investment_round'],
                    'investor_expertise': record['investor_expertise'].split(','),
                    'engagement_lengths': record['engagement_lengths'].split(','),
                    'engagement_models': record['engagement_models'].split(','),
                    'revenue_models': record['revenue_models'].split(','),
                    'revenue': record['revenue'],
                    'profit_margin': record['profit_margin'],
                    'churn_rate': record['churn_rate'],
                    'intellectual_properties': record['intellectual_properties'].split(','),
                    'competitive_advantage': record['competitive_advantage'],
                    'current_challenges': record['current_challenges'],
                    'user' : record['user']
                }
                return startup_profile_data

            else:
                raise ValueError(f"No profile found for user: {st.session_state.get('username')}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_investor_profile():
    try:
        # Assuming you have an established database connection named 'conn'
        with conn.session as s:
            # Query to fetch the investor profile of a particular user
            result = s.execute('''
                SELECT * FROM investor_profiles WHERE user = :user;
            ''', {'user': st.session_state.get('username')})

            # Fetching the first (and presumably only) record that matches the user
            record = result.fetchone()

            if record:
                # Constructing a dictionary to hold the investor profile data
                investor_profile_data = {
                    'investment_company': record['investment_company'],
                    'investor_type': record['investor_type'].split(','),
                    'investor_description': record['investor_description'],
                    'investor_expertise': record['investor_expertise'].split(','),
                    'preferred_attributes': record['preferred_attributes'].split(','),
                    'preferred_business_priority': record['preferred_business_priority'].split(','),
                    'preferred_founder_gender': record['preferred_founder_gender'].split(','),
                    'preferred_investment_round': record['preferred_investment_round'].split(','),
                    'preferred_industry': record['preferred_industry'].split(','),
                    'preferred_country': record['preferred_country'].split(','),
                    'min_investment': record['min_investment'],
                    'max_investment': record['max_investment'],
                    'past_investments': record['past_investments'],
                    'successful_exits': record['successful_exits'],
                    'preferred_startup_age_min': record['preferred_startup_age_min'],
                    'preferred_startup_age_max': record['preferred_startup_age_max'],
                    'preferred_business_model': record['preferred_business_model'].split(','),
                    'preferred_business_stage': record['preferred_business_stage'].split(','),
                    'preferred_engagement_length': record['preferred_engagement_length'].split(','),
                    'preferred_engagement_model': record['preferred_engagement_model'].split(','),
                    'preferred_team_size_min': record['preferred_team_size_min'],
                    'preferred_team_size_max': record['preferred_team_size_max'],
                    'user' : record['user']
                }
                return investor_profile_data

            else:
                user = st.session_state.get('username')
                raise ValueError(f"No profile found for user: {user}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def get_investors():
    try:
        # Assuming you have an established database connection named 'conn'
        with conn.session as s:
            # Query to fetch the investor profile of a particular user
            result = s.execute('''
                SELECT * FROM investor_profiles;
            ''')

            # Fetching the first (and presumably only) record that matches the user
            records = result.fetchall()

            if records:
                # Constructing a dictionary to hold the investor profile data
                investor_profile_data = [{
                    'investment_company': record['investment_company'],
                    'investor_type': record['investor_type'].split(','),
                    'investor_description': record['investor_description'],
                    'investor_expertise': record['investor_expertise'].split(','),
                    'preferred_attributes': record['preferred_attributes'].split(','),
                    'preferred_business_priority': record['preferred_business_priority'].split(','),
                    'preferred_founder_gender': record['preferred_founder_gender'].split(','),
                    'preferred_investment_round': record['preferred_investment_round'].split(','),
                    'preferred_industry': record['preferred_industry'].split(','),
                    'preferred_country': record['preferred_country'].split(','),
                    'min_investment': record['min_investment'],
                    'max_investment': record['max_investment'],
                    'past_investments': record['past_investments'],
                    'successful_exits': record['successful_exits'],
                    'preferred_startup_age_min': record['preferred_startup_age_min'],
                    'preferred_startup_age_max': record['preferred_startup_age_max'],
                    'preferred_business_model': record['preferred_business_model'].split(','),
                    'preferred_business_stage': record['preferred_business_stage'].split(','),
                    'preferred_engagement_length': record['preferred_engagement_length'].split(','),
                    'preferred_engagement_model': record['preferred_engagement_model'].split(','),
                    'preferred_team_size_min': record['preferred_team_size_min'],
                    'preferred_team_size_max': record['preferred_team_size_max'],
                    'user' : record['user']
                } for record in records]
                return investor_profile_data

            else:
                raise ValueError(f"No records found")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def get_startups():
    try:
        # Assuming you have an established database connection named 'conn'
        with conn.session as s:
            # Query to fetch the startup profile of a particular user
            result = s.execute('''
                SELECT * FROM startup_profiles;
            ''')

            # Fetching the first (and presumably only) record that matches the user
            records = result.fetchall()

            if records:
                # Constructing a dictionary to hold the startup profile data
                startup_profile_data = [{
                    'startup_company': record['startup_company'],
                    'startup_website': record['startup_website'],
                    'startup_stage': record['startup_stage'],
                    'startup_industries': record['startup_industries'].split(','),
                    'startup_countries': record['startup_countries'],
                    'startup_age': record['startup_age'],
                    'mission': record['mission'],
                    'long_term_goals': record['long_term_goals'],
                    'current_capital': record['current_capital'],
                    'current_investment': record['current_investment'],
                    'investment_needed': record['investment_needed'],
                    'business_priorities': record['business_priorities'].split(','),
                    'founder_name': record['founder_name'],
                    'founder_positions': record['founder_positions'].split(','),
                    'founder_gender': record['founder_gender'],
                    'team_size': record['team_size'],
                    'key_team_expertise': record['key_team_expertise'].split(','),
                    'product_description': record['product_description'],
                    'business_models': record['business_models'].split(','),
                    'product_stages': record['product_stages'],
                    'monthly_users': record['monthly_users'],
                    'investor_attributes': record['investor_attributes'].split(','),
                    'investment_round': record['investment_round'],
                    'investor_expertise': record['investor_expertise'].split(','),
                    'engagement_lengths': record['engagement_lengths'].split(','),
                    'engagement_models': record['engagement_models'].split(','),
                    'revenue_models': record['revenue_models'].split(','),
                    'revenue': record['revenue'],
                    'profit_margin': record['profit_margin'],
                    'churn_rate': record['churn_rate'],
                    'intellectual_properties': record['intellectual_properties'].split(','),
                    'competitive_advantage': record['competitive_advantage'],
                    'current_challenges': record['current_challenges'],
                    'user' : record['user']
                } for record in records]
                return startup_profile_data

            else:
                raise ValueError(f"No records found")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_random_user(length_=7):
    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length_))
    return str(res)

def load_dummy_investor_data(lst):
    def create_investor_profile(data):
        try:
            # Assuming you have an established database connection named 'conn'
            with conn.session as s:
                # Table creation for investor profiles
                s.execute('''
                    CREATE TABLE IF NOT EXISTS investor_profiles (
                        investment_company TEXT,
                        investor_type TEXT,
                        investor_description TEXT,
                        investor_expertise TEXT,
                        preferred_attributes TEXT,
                        preferred_business_priority TEXT,
                        preferred_founder_gender TEXT,
                        preferred_investment_round TEXT,
                        preferred_industry TEXT,
                        preferred_country TEXT,
                        min_investment REAL,
                        max_investment REAL,
                        past_investments REAL,
                        successful_exits INTEGER,
                        preferred_startup_age_min  INTEGER,
                        preferred_startup_age_max INTEGER,
                        preferred_business_model TEXT,
                        preferred_business_stage TEXT,
                        preferred_engagement_length TEXT,
                        preferred_engagement_model TEXT,
                        preferred_team_size_min INTEGER,
                        preferred_team_size_max INTEGER,
                        user TEXT PRIMARY KEY
                    );
                ''')

                # Delete existing investor record
                s.execute('delete from investor_profiles where user = :user;', {'user': data['user']})

                # Inserting new investor profile
                s.execute('''
                    INSERT INTO investor_profiles (
                        investment_company, investor_type, investor_description, investor_expertise, preferred_attributes,
                        preferred_business_priority, preferred_founder_gender, preferred_investment_round, preferred_industry,
                        preferred_country, min_investment, max_investment, past_investments, successful_exits, 
                        preferred_startup_age_min, preferred_startup_age_max, preferred_business_model, preferred_business_stage, 
                        preferred_engagement_length, preferred_engagement_model, preferred_team_size_min, preferred_team_size_max, user
                    ) VALUES (
                        :investment_company, :investor_type, :investor_description, :investor_expertise, :preferred_attributes,
                        :preferred_business_priority, :preferred_founder_gender, :preferred_investment_round, :preferred_industry,
                        :preferred_country, :min_investment, :max_investment, :past_investments, :successful_exits, 
                        :preferred_startup_age_min, :preferred_startup_age_max, :preferred_business_model, :preferred_business_stage, 
                        :preferred_engagement_length, :preferred_engagement_model, :preferred_team_size_min, :preferred_team_size_max, :user
                    );
                ''', {
                        'investment_company': data['investment_company'],
                        'investor_type': ','.join(data['investor_type']),
                        'investor_description': data['investor_description'],
                        'investor_expertise': ','.join(data['investor_expertise']),
                        'preferred_attributes': ','.join(data['preferred_attributes']),
                        'preferred_business_priority': ','.join(data['preferred_business_priority']),
                        'preferred_founder_gender': ','.join(data['preferred_founder_gender']),
                        'preferred_investment_round': ','.join(data['preferred_investment_round']),
                        'preferred_industry': ','.join(data['preferred_industry']),
                        'preferred_country': ','.join(data['preferred_country']),
                        'min_investment': data['min_investment'],
                        'max_investment': data['max_investment'],
                        'past_investments': data['past_investments'],
                        'successful_exits': data['successful_exits'],
                        'preferred_startup_age_min': data['preferred_startup_age_min'],
                        'preferred_startup_age_max': data['preferred_startup_age_max'],
                        'preferred_business_model': ','.join(data['preferred_business_model']),
                        'preferred_business_stage': ','.join(data['preferred_business_stage']),
                        'preferred_engagement_length': ','.join(data['preferred_engagement_length']),
                        'preferred_engagement_model': ','.join(data['preferred_engagement_model']),
                        'preferred_team_size_min': data['preferred_team_size_min'],
                        'preferred_team_size_max': data['preferred_team_size_max'],
                        'user': data['user']
                    })

                s.commit()

        except Exception as e:
            return str(e)  # Return the error message

        return None  # Return None if everything is successful

    for entry in lst:
        # Generate a random user for each entry
        entry['user'] = generate_random_user()
        create_investor_profile(entry)


import random
import string
import streamlit as st  # Importing streamlit for session management

def generate_random_user(length_=7):
    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length_))
    return str(res)

def load_dummy_startup_data(lst):
    def create_startup_profile(data):
        try:
            # Assuming you have an established database connection named 'conn'
            with conn.session as s:
                # Table creation for startup profiles
                s.execute('''
                    CREATE TABLE IF NOT EXISTS startup_profiles (
                        startup_company TEXT,
                        startup_website TEXT,
                        startup_stage TEXT,
                        startup_industries TEXT,
                        startup_countries TEXT,
                        startup_age INTEGER,
                        mission TEXT,
                        long_term_goals TEXT,
                        current_capital REAL,
                        current_investment REAL,
                        investment_needed REAL,
                        business_priorities TEXT,
                        founder_name TEXT,
                        founder_positions TEXT,
                        founder_gender TEXT,
                        team_size INTEGER,
                        key_team_expertise TEXT,
                        product_description TEXT,
                        business_models TEXT,
                        product_stages TEXT,
                        monthly_users INTEGER,
                        investor_attributes TEXT,
                        investment_round TEXT,
                        investor_expertise TEXT,
                        engagement_lengths TEXT,
                        engagement_models TEXT,
                        revenue_models TEXT,
                        revenue REAL,
                        profit_margin REAL,
                        churn_rate REAL,
                        intellectual_properties TEXT,
                        competitive_advantage TEXT,
                        current_challenges TEXT,
                        user TEXT PRIMARY KEY
                    );
                ''')

                # Delete existing startup record
                s.execute('delete from startup_profiles where user = :user;', {'user': data['user']})

                # Inserting new startup profile
                s.execute('''
                    INSERT INTO startup_profiles (
                        startup_company, startup_website, startup_stage, startup_industries, startup_countries,
                        startup_age, mission, long_term_goals, current_capital, current_investment,
                        investment_needed, business_priorities, founder_name, founder_positions, founder_gender,
                        team_size, key_team_expertise, product_description, business_models, product_stages,
                        monthly_users, investor_attributes, investment_round, investor_expertise,
                        engagement_lengths, engagement_models, revenue_models, revenue,
                        profit_margin, churn_rate, intellectual_properties, competitive_advantage,
                        current_challenges,user
                    ) VALUES (
                        :startup_company, :startup_website, :startup_stage, :startup_industries, :startup_countries,
                        :startup_age, :mission, :long_term_goals, :current_capital, :current_investment,
                        :investment_needed, :business_priorities, :founder_name, :founder_positions, :founder_gender,
                        :team_size, :key_team_expertise, :product_description, :business_models, :product_stages,
                        :monthly_users, :investor_attributes, :investment_round, :investor_expertise,
                        :engagement_lengths, :engagement_models, :revenue_models, :revenue,
                        :profit_margin, :churn_rate, :intellectual_properties, :competitive_advantage,
                        :current_challenges,:user
                    );
                ''', {
                        'startup_company': data['startup_company'],
                        'startup_website': data['startup_website'],
                        'startup_stage': data['startup_stage'],
                        'startup_industries': ','.join(data['startup_industries']),
                        'startup_countries': data['startup_countries'],
                        'startup_age': data['startup_age'],
                        'mission': data['mission'],
                        'long_term_goals': data['long_term_goals'],
                        'current_capital': data['current_capital'],
                        'current_investment': data['current_investment'],
                        'investment_needed': data['investment_needed'],
                        'business_priorities': ','.join(data['business_priorities']),
                        'founder_name': data['founder_name'],
                        'founder_positions': ','.join(data['founder_positions']),
                        'founder_gender': data['founder_gender'],
                        'team_size': data['team_size'],
                        'key_team_expertise': ','.join(data['key_team_expertise']),
                        'product_description': data['product_description'],
                        'business_models': ','.join(data['business_models']),
                        'product_stages': data['product_stages'],
                        'monthly_users': data['monthly_users'],
                        'investor_attributes': ','.join(data['investor_attributes']),
                        'investment_round': data['investment_round'],
                        'investor_expertise': ','.join(data['investor_expertise']),
                        'engagement_lengths': ','.join(data['engagement_lengths']),
                        'engagement_models': ','.join(data['engagement_models']),
                        'revenue_models': ','.join(data['revenue_models']),
                        'revenue': data['revenue'],
                        'profit_margin': data['profit_margin'],
                        'churn_rate': data['churn_rate'],
                        'intellectual_properties': ','.join(data['intellectual_properties']),
                        'competitive_advantage': data['competitive_advantage'],
                        'current_challenges': data['current_challenges'],
                        'user': data['user']
                    })

                s.commit()

        except Exception as e:
            return str(e)  # Return the error message

        return None  # Return None if everything is successful

    for entry in lst:
        # Generate a random user for each entry
        entry['user'] = generate_random_user()
        create_startup_profile(entry)



# Helper function to generate random selections from a list
def random_select(options_list, max_selections=3):
    selections = random.sample(options_list, k=random.randint(1, max_selections))
    return selections

def generate_dummy_startup_data(count=100):
    # Generating the dummy data
    dummy_startup_data = []
    for i in range(count):
        startup_data = {
            'startup_company': f'Startup{i} Inc.',
            'startup_website': f'https://startup{i}.com',
            'startup_stage': random.choice(STARTUP_STAGES),
            'startup_industries': random_select(INDUSTRIES, 2),
            'startup_countries': random.choice(COUNTRIES),
            'startup_age': random.randint(1, 10),
            'mission': f'Mission statement of Startup{i}...',
            'long_term_goals': f'Long term goals of Startup{i}...',
            'current_capital': random.uniform(10000, 50000),
            'current_investment': random.uniform(10000, 50000),
            'investment_needed': random.uniform(10000, 50000),
            'business_priorities': random_select(BUSINESS_PRIORITIES, 2),
            'founder_name': f'Founder{i} Name',
            'founder_positions': random_select(FOUNDER_POSITIONS, 2),
            'founder_gender': random.choice(GENDERS),
            'team_size': random.randint(5, 50),
            'key_team_expertise': random_select(KEY_TEAM_EXPERTISE, 3),
            'product_description': f'Product description of Startup{i}...',
            'business_models': random_select(BUSINESS_MODELS, 2),
            'product_stages': random.choice(PRODUCT_STAGES),
            'monthly_users': random.randint(1000, 1000000),
            'investor_attributes': random_select(PREFERRED_ATTRIBUTES, 3),
            'investment_round': random.choice(INVESTMENT_ROUNDS),
            'investor_expertise': random_select(INVESTOR_EXPERTISE, 3),
            'engagement_lengths': random_select(ENGAGEMENT_LENGTHS, 1),
            'engagement_models': random_select(ENGAGEMENT_MODELS, 2),
            'revenue_models': random_select(REVENUE_MODELS, 2),
            'revenue': random.uniform(0, 100000),
            'profit_margin': random.uniform(0.05, 0.4),
            'churn_rate': random.uniform(5, 25),
            'intellectual_properties': random_select(INTELLECTUAL_PROPERTY, 2),
            'competitive_advantage': f'Competitive advantage of Startup{i}...',
            'current_challenges': f'Current challenges of Startup{i}...'
        }
        dummy_startup_data.append(startup_data)

    return dummy_startup_data


def generate_dummy_investor_data(count=100):
    # Generate x dummy investor data entries
    dummy_investor_data = []
    for i in range(count):
        dummy_investor_data.append(
            {
                'investment_company': f'Investment Company {i+1}',
                'investor_type': random_select(INVESTOR_TYPES),
                'investor_description': f'Investing in early-stage startups in the {random.choice(INDUSTRIES)} sector.',
                'investor_expertise': random_select(INVESTOR_EXPERTISE),
                'preferred_attributes': random_select(PREFERRED_ATTRIBUTES),
                'preferred_business_priority': random_select(BUSINESS_PRIORITIES),
                'preferred_founder_gender': random_select(GENDERS, max_selections=2),
                'preferred_investment_round': random_select(INVESTMENT_ROUNDS),
                'preferred_industry': random_select(INDUSTRIES),
                'preferred_country': random_select(COUNTRIES),
                'min_investment': round(random.uniform(10_000, 500_000), 2),
                'max_investment': round(random.uniform(500_000, 2_000_000), 2),
                'past_investments': round(random.uniform(1_000_000, 10_000_000), 2),
                'successful_exits': random.randint(0, 10),
                'preferred_startup_age_min': random.randint(0, 5),
                'preferred_startup_age_max': random.randint(5, 10),
                'preferred_business_model': random_select(BUSINESS_MODELS),
                'preferred_business_stage': random_select(PRODUCT_STAGES),
                'preferred_engagement_length': random_select(ENGAGEMENT_LENGTHS, max_selections=1),
                'preferred_engagement_model': random_select(ENGAGEMENT_MODELS),
                'preferred_team_size_min': random.randint(1, 10),
                'preferred_team_size_max': random.randint(10, 50),
            }
        )

    return dummy_investor_data


def sample_investors(count=100):
    load_dummy_investor_data(generate_dummy_investor_data(count))
    return True


def sample_startups(count=100):
    load_dummy_startup_data(generate_dummy_startup_data(count))
    return True