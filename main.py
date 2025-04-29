import streamlit as st
from db import create_table, add_record, get_all_records, search_records, delete_record, update_record
from datetime import datetime

create_table()

# --- CSS ---
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }
        h1, h2, h3 {
            margin-top: 0rem;
        }
    </style>
""", unsafe_allow_html=True)


if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    # --- Login Section ---
    def login():
        st.title("🔐 Toll Plaza Login")

        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = False

        if not st.session_state['logged_in']:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")

                if submitted:
                    if username == "admin" and password == "admin123":
                        st.session_state['logged_in'] = True
                        st.success("Login Successful")
                        st.rerun()  # Important: go to next page immediately
                    else:
                        st.error("Invalid credentials")
            st.stop()
    login()
    st.stop()


# --- Main App ---
st.title("🚧 Toll Plaza Management System")

menu = ["View/Search/Edit Records", "Add New Record"]
choice = st.sidebar.selectbox("Menu", menu)


if choice == "View/Search/Edit Records":
    st.subheader("📋 View, Search, Edit or Delete Records")

    search_term = st.text_input("Search by Vehicle Number")

    if search_term:
        records = search_records(search_term)
    else:
        records = get_all_records()

    if records:
        for record in records:
            with st.expander(f"Vehicle: {record[1]} | Amount: ₹{record[3]}"):
                st.write(f"**Vehicle Type:** {record[2]}")
                st.write(f"**Date:** {record[4]}")
                st.write(f"**Lane Number:** {record[5]}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{record[0]}"):
                        with st.form(f"edit_form_{record[0]}"):
                            new_vehicle_number = st.text_input("Vehicle Number", record[1])
                            new_vehicle_type = st.selectbox("Vehicle Type", ["Car", "Truck", "Bus", "Bike", "Other"],
                                                            index=["Car", "Truck", "Bus", "Bike", "Other"].index(
                                                                record[2]))
                            new_toll_amount = st.number_input("Toll Amount", value=float(record[3]))
                            new_timestamp = st.date_input("Date", datetime.strptime(record[4], "%Y-%m-%d"))
                            new_lane_number = st.text_input("Lane Number", record[5])

                            submit_update = st.form_submit_button("Update Record")
                            if submit_update:
                                update_record(record[0], new_vehicle_number, new_vehicle_type, new_toll_amount,
                                              new_timestamp.strftime("%Y-%m-%d"), new_lane_number)
                                st.success("Record updated successfully!")
                                st.rerun()

                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{record[0]}"):
                        delete_record(record[0])
                        st.success("Record deleted successfully!")
                        st.rerun()

    else:
        st.info("No records found.")

elif choice == "Add New Record":
    st.subheader("➕ Add Toll Record")

    vehicle_number = st.text_input("Vehicle Number")
    vehicle_type = st.selectbox("Vehicle Type", ["Car", "Truck", "Bus", "Bike", "Other"])
    toll_amount = st.number_input("Toll Amount", min_value=0.0)
    timestamp = st.date_input("Date")  # you could also automatically use datetime.now()
    lane_number = st.text_input("Lane Number")

    if st.button("Add Record"):
        add_record(vehicle_number, vehicle_type, toll_amount, timestamp.strftime("%Y-%m-%d"), lane_number)
        st.success("Record Added Successfully!")

if st.sidebar.button("🚪 Logout"):
        st.session_state['logged_in'] = False
        st.success("Logged Out Successfully")
        st.rerun()