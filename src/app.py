import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart City Intelligence",
    page_icon="🏙️",
    layout="wide"
)

pages = {
    "My Dashboard": [
        st.Page("pages/Home.py", title="Home"),
        st.Page("pages/Traffic.py", title="Traffic"),
        st.Page("pages/Complaints.py", title="Complaints"),
        st.Page("pages/Air_Quality.py", title="Air Quality"),
        
    ]
}

pg = st.navigation(pages)
pg.run()



