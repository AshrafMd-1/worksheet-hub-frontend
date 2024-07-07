import streamlit as st

from menu import menu

st.set_page_config(page_title="About", page_icon="❓", layout="centered")

menu()

if "flag_s" in st.session_state:
    del st.session_state.flag_s

if "flag_b" in st.session_state:
    del st.session_state.flag_b

st.markdown("""
### About
This is a tool to help you search for worksheets by roll number.

### Version
1.0.3 - 2024-07-07

### Major Fixes
- Offloaded bulk search to external server for faster processing [ 1m 12s ➡️ 15s ]
- Increased bulk search limit to 80 roll numbers
- UI improvements

### Developer
- ##### [Ashraf MD](https://www.linkedin.com/in/ashraf-mohammed-75932823a/)

---
""")

st.markdown("""# Made with ❤️ by :rainbow[GDSC IARE]""")

st.html("""
<h3>
    <a href="https://gdsc.community.dev/institute-of-aeronautical-engineering-hyderabad-india/">
        [ JOIN US ]    
    </a>
</h3>
""")
