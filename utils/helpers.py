import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from streamlit.source_util import (
    page_icon_and_name, 
    calc_md5, 
    get_pages,
    _on_pages_changed
)

def delete_page(main_script_path_str, page_name):

    current_pages = get_pages(main_script_path_str)

    for key, value in current_pages.items():
        if value['page_name'] == page_name:
            del current_pages[key]
            break
        else:
            pass
    _on_pages_changed.send()

def add_page(main_script_path_str, page_name):
    
    pages = get_pages(main_script_path_str)
    main_script_path = Path(main_script_path_str)
    pages_dir = main_script_path.parent / "pages"
    script_path = [f for f in pages_dir.glob("*.py") if f.name.find(page_name) != -1][0]
    script_path_str = str(script_path.resolve())
    pi, pn = page_icon_and_name(script_path)
    psh = calc_md5(script_path_str)
    pages[psh] = {
        "page_script_hash": psh,
        "page_name": pn,
        "icon": pi,
        "script_path": script_path_str,
    }
    _on_pages_changed.send()


def delete_all_pages():
    delete_page("pages", "Sign_In")
    delete_page("pages", "Registration")
    delete_page("pages", "Startup_Profile")
    delete_page("pages", "Investor_Profile")
    delete_page("pages", "Explore_Investors")
    delete_page("pages", "Explore_Startups")
    delete_page("pages", "templates")
    delete_page("pages", "Recommend_Investors")
    delete_page("pages", "Investors_Details")
    delete_page("pages", "Recommend_Startups")
    delete_page("pages", "Startups_Details")
    delete_page("pages", "templates")

def add_investor_pages():
    delete_all_pages()
    add_page("pages", "Sign_In")
    add_page("pages", "Investor_Profile")
    add_page("pages", "Explore_Startups")
    add_page("pages", "Recommend_Startups")
    add_page("pages", "Startups_Details")


def add_startup_pages():
    delete_all_pages()
    add_page("pages", "Sign_In")
    add_page("pages", "Startup_Profile")
    add_page("pages", "Explore_Investors")
    add_page("pages", "Recommend_Investors")
    add_page("pages", "Investors_Details")


def add_home_page():
    delete_all_pages()
    add_page("pages", "Sign_In")
    add_page("pages", "Registration")