import streamlit as st

st.set_page_config(
    page_title="Voka",
    page_icon="👋",
)

st.write("# Welcome to project for Voka! 👋")

st.sidebar.success("Select a page above")

st.markdown(
    """
    This is the project of Floris, Emma, Storm, Marlon and Max for the course Data Engineering Project II at HoGent.

    In the sidebar you can select pages.

    View Data: View the data in the database.

    Recommendations: Upload a csv file with a campaign and get recommendations for contacts.
"""
)