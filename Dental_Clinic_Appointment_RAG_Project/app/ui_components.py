import streamlit as st


def render_faq_search(qa_chain):
    """Sidebar FAQ search box"""
    query = st.sidebar.text_input("Search FAQs")
    if query:
        answer = qa_chain.run(query)
        st.sidebar.markdown(f"**Answer:** {answer}")


def render_patient_form(slots, on_submit):
    """Patient booking form with schedule radio buttons"""
    with st.form("patient_form", clear_on_submit=True):
        name = st.text_input("Patient Name")
        address = st.text_input("Address")
        phone = st.text_input("Phone Number")
        treatment = st.text_input("Treatment Required")

        # schedule radio
        labels = []
        for slot in slots:
            label = f"Dr.{slot['doctor_id']} - {slot['schedule_date']} {slot['start_time']}"
            labels.append(label)

        selected = st.radio("Select Slot", labels)
        submitted = st.form_submit_button("Submit")
        if submitted:
            on_submit(name, address, phone, treatment, selected)
