import json
import re
import time

import pandas as pd
import streamlit as st

from menu import menu
from utils import roman_to_digits, search_bulk_worksheet_v2, bulk_rolls_count

st.set_page_config(page_title="Bulk", page_icon="📖", layout="centered")

menu()

if "flag_s" in st.session_state:
    del st.session_state.flag_s

st.title('Bulk Search')
st.write('Search for multiple worksheets by a range of roll numbers. **{max 80 roll numbers}**')

if "flag_b" not in st.session_state:
    st.session_state.flag_b = 0

if "pdf_data_b" not in st.session_state:
    st.session_state.pdf_data_b = {}

if st.session_state.flag_b == 0:
    with st.form(key='bulk_search'):
        roll_number_first = st.text_input('Enter first roll number', key=1)
        roll_number_last = st.text_input('Enter last roll number', key=2)
        check = st.form_submit_button('Submit')
        if check:
            roll_number_first = roll_number_first.upper()
            roll_number_last = roll_number_last.upper()
            if not roll_number_first or not roll_number_last:
                st.error('Please enter both roll numbers.')
                st.stop()
            if roll_number_first == roll_number_last:
                st.error('Roll numbers cannot be the same.')
                st.stop()
            if roll_number_first[:8] != roll_number_last[:8]:
                st.error('First 8 characters of roll numbers should be same.')
                st.stop()
            pattern = r'^\d+A\d+\w*$'
            if re.match(pattern, roll_number_first.upper()) and re.match(pattern, roll_number_last.upper()) and len(
                    roll_number_first) == 10 and len(roll_number_last) == 10:
                bulk_roll_count = bulk_rolls_count(roll_number_first, roll_number_last)
                exceed_status = False
                if bulk_roll_count["status"] == "exceeded":
                    exceed_status = True
                    roll_number_last = bulk_roll_count["roll"].upper()
                st.session_state.pdf_data_b = {
                    "roll_number_first": roll_number_first.upper(),
                    "roll_number_last": roll_number_last.upper(),
                    "exceeded": exceed_status
                }
                st.session_state.flag_b = 1
                st.rerun()
            else:
                st.error('Invalid roll number. Please enter a valid roll number.')

if st.session_state.flag_b > 0:
    st.text_input('Roll number first', value=st.session_state.pdf_data_b["roll_number_first"], key=1, disabled=True)
    st.text_input('Roll number last', value=st.session_state.pdf_data_b["roll_number_last"], key=2, disabled=True)
    if st.session_state.pdf_data_b["exceeded"]:
        st.info(
            f"You can search for maximum 80 roll numbers. Auto assigned to {st.session_state.pdf_data_b['roll_number_last']}")
    edit = st.button('Edit')
    if edit:
        st.session_state.flag_b = 0
        st.rerun()

if st.session_state.flag_b > 0:
    regulation = st.selectbox(
        "Regulation",
        ("BT23", "UG20"),
        index=None,
        placeholder="Select a regulation"
    )
    if regulation:
        st.session_state.pdf_data_b["regulation"] = regulation
        roll_number = st.session_state.pdf_data_b["roll_number_first"]
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
            st.session_state.pdf_data_b["semester"] = roman_to_digits(semester.split()[0])
            subject_data_raw = data[roll_number[6:8]][semester]['Practical']
            subject = st.selectbox(
                "Subject",
                subject_data_raw.values(),
                index=None,
                placeholder="Select a subject"
            )
            if subject:
                st.session_state.pdf_data_b["subject"] = next((k for k, v in subject_data_raw.items() if v == subject),
                                                              None)
                week_no = st.number_input('Week number', min_value=1, max_value=15)
                if week_no:
                    st.session_state.pdf_data_b["week_no"] = week_no
                    search = st.button('Search')
                    if search:
                        start_time = time.time()
                        with st.spinner('Searching...'):
                            pdf_urls = search_bulk_worksheet_v2(
                                st.session_state.pdf_data_b["roll_number_first"],
                                st.session_state.pdf_data_b["roll_number_last"],
                                st.session_state.pdf_data_b["semester"],
                                st.session_state.pdf_data_b["subject"],
                                st.session_state.pdf_data_b["week_no"]
                            )
                            if pdf_urls:
                                df = pd.DataFrame(pdf_urls, columns=["Roll Number", "Link"])
                                df_link_available = df[df["Link"] != "Not found"]
                                if df_link_available.empty:
                                    st.write('Worksheets not found.')
                                else:
                                    df_link_available = df_link_available.reset_index(drop=True)
                                    df_link_available.index += 1
                                    end_time = time.time()
                                    execution_time = end_time - start_time
                                    st.write(f"Execution time: {execution_time:.2f} seconds")
                                    st.data_editor(df_link_available, disabled=True, use_container_width=True,
                                                   column_config={
                                                       "Link": st.column_config.LinkColumn(
                                                           "Links", display_text="Open worksheet"
                                                       ),
                                                   })
                            else:
                                st.error('Error occurred while searching for worksheets.')
