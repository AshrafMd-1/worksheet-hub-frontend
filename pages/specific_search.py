import json
import re
import time

import streamlit as st

from menu import menu
from utils import roman_to_digits, search_specific_worksheet

st.set_page_config(page_title="Specific", page_icon="📃", layout="centered")

menu()

if "flag_b" in st.session_state:
    del st.session_state.flag_b

st.title('Specific Search')
st.write('Search for a worksheet by roll number.')

if "flag_s" not in st.session_state:
    st.session_state.flag_s = 0

if "pdf_data_s" not in st.session_state:
    st.session_state.pdf_data_s = {}

if st.session_state.flag_s == 0:
    roll_number = st.text_input('Enter roll number')
    st.session_state.pdf_data_s = {
        "roll_number": roll_number.upper()
    }
    check = st.button('Check')
    if check:
        pattern = r'^\d+A\d+\d*$'
        if re.match(pattern, roll_number.upper()) and len(roll_number) == 10:
            st.session_state.flag_s = 1
            st.rerun()
        else:
            st.error('Invalid roll number. Please enter a valid roll number.')

if st.session_state.flag_s > 0:
    st.text_input('Roll number', value=st.session_state.pdf_data_s["roll_number"], key=1, disabled=True)
    edit = st.button('Edit')
    if edit:
        st.session_state.flag_s = 0
        st.rerun()

if st.session_state.flag_s > 0:
    regulation = st.selectbox(
        "Regulation",
        ("BT23", "UG20"),
        index=None,
        placeholder="Select a regulation"
    )
    if regulation:
        st.session_state.pdf_data_s["regulation"] = regulation
        roll_number = st.session_state.pdf_data_s["roll_number"]
        with open(f'data/{regulation.lower()}.json', 'r') as file:
            data = json.load(file)
        try:
            semester_data = data[roll_number[6:8]].keys()
        except KeyError:
            st.error('No data found for the given roll number.')
            st.stop()
        semester = st.selectbox(
            "Semester",
            semester_data,
            index=None,
            placeholder="Select a semester"
        )
        if semester:
            st.session_state.pdf_data_s["semester"] = roman_to_digits(semester.split()[0])
            subject_data_raw = data[roll_number[6:8]][semester]['Practical']
            subject = st.selectbox(
                "Subject",
                subject_data_raw.values(),
                index=None,
                placeholder="Select a subject"
            )
            if subject:
                st.session_state.pdf_data_s["subject"] = next((k for k, v in subject_data_raw.items() if v == subject),
                                                              None)
                week_no = st.number_input('Week number', min_value=1, max_value=15)
                if week_no:
                    st.session_state.pdf_data_s["week_no"] = week_no
                    search = st.button('Search')
                    if search:
                        start_time = time.time()
                        with st.spinner('Searching...'):
                            pdf_url = search_specific_worksheet(
                                st.session_state.pdf_data_s["roll_number"],
                                st.session_state.pdf_data_s["semester"],
                                st.session_state.pdf_data_s["subject"],
                                st.session_state.pdf_data_s["week_no"]
                            )
                            end_time = time.time()
                            execution_time = end_time - start_time
                            st.write(f"Execution time: {execution_time:.2f} seconds")
                            if pdf_url:
                                st.write(f'### [Open worksheet]({pdf_url})')
                            else:
                                st.write('Worksheet not found.')
