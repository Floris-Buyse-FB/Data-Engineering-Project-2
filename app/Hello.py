import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Voka",
    page_icon="👋",
)

# Header
st.image("./images/voka.png", width=300, )
st.title("Welcome to the Voka Project! 👋")

# Sidebar
# st.sidebar.success("Select a page above")

# Main content
st.markdown(
    """
    ## About

    This project is developed by Floris, Emma, Storm, Marlon, and Max for the course Data Engineering Project II at HoGent.

    ### Navigation

    - **Add Data:** Add data to the database.
    - **View Data:** View the data in the database.
    - **Lookalikes:** Generate lookalikes for a contact.
    - **Recommendations:** Upload a CSV file with a campaign and get recommendations for contacts.
    - **Email Generator:** Generate a personalized email for a contact.

    ## Instructions

    Explore the different pages using the sidebar. Each page provides specific functionalities related to the Voka project.

    Feel free to contribute and enhance the project!

    Enjoy your exploration! 🚀

    ### Project Team
    #### Floris | Emma | Storm | Marlon | Max
"""
)
