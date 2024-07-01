import streamlit as st

from menu import menu

st.set_page_config(page_title="About", page_icon="❓", layout="centered")

menu()

st.markdown("""
## About
This is a tool to help you search for worksheets by roll number.

## Version
1.0.0 - 2024-07-01

## Contributors
- [Ashraf MD](https://www.linkedin.com/in/ashraf-mohammed-75932823a/) **Tech Lead**
""")

st.markdown("""# Made with ❤️ by :rainbow[GDSC IARE]""")

st.markdown("""> https://gdsc.community.dev/institute-of-aeronautical-engineering-hyderabad-india/""")
