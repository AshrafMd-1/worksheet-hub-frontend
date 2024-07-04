import streamlit as st

from menu import menu

st.set_page_config(page_title="Home", page_icon="🎉", layout="centered")

menu()

st.title('Welcome to the Worksheet Hub')
st.write('This is a tool to help you search for worksheets by roll number.')

st.divider()

st.header('Specific Search')
st.write('Search for a worksheet by roll number.')

st.header('Bulk Search')
st.write('Search for multiple worksheets by a range of roll numbers.')

st.sidebar.markdown("""
<style>
    a[href="https://streamlit.io/cloud"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

