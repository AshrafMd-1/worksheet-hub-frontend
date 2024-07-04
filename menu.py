import streamlit as st


def menu():
    st.sidebar.markdown("# :blue[Worksheet Hub]")
    st.sidebar.page_link("pages/specific_search.py", label="Specific Search")
    st.sidebar.page_link("pages/bulk_search.py", label="Bulk Search")
    st.sidebar.page_link("pages/about.py", label="About")
    st.sidebar.markdown("""
    <style>
        a[href="https://streamlit.io/cloud"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
