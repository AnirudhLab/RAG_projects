# app/main.py

import os
import streamlit as st
import pandas as pd
from datetime import date
from dotenv import load_dotenv

from ingestion.pdf_loader import load_and_split
from rag.embeddings import get_embeddings
from rag.vector_store import init_vector_store
from rag.sql_store import get_db_conn, fetch_upcoming_slots, book_slot
from rag.agent import AppointmentAgent
from langchain.chat_models import ChatOpenAI


# ─── Load .env ─────────────────────────────────────────────────────────────────
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'dental_clinic'),
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FAQ_PDF_PATH     = os.getenv('FAQ_PDF_PATH', 'data/clinic_faq.pdf')
VECTORSTORE_DIR  = os.getenv('VECTORSTORE_DIR', 'vectorstore')

# ─── FAQ QA Chain ──────────────────────────────────────────────────────────────
@st.cache_resource
def init_faq_qa():
    docs       = load_and_split(FAQ_PDF_PATH)
    embeddings = get_embeddings(OPENAI_API_KEY)
    vs         = init_vector_store(docs, embeddings, VECTORSTORE_DIR)
    agent      = AppointmentAgent(vs, None, OPENAI_API_KEY)
    return agent.qa_chain

# ─── App ──────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(page_title="Dental Clinic Appointment Manager", layout="wide")
    st.title("🦷 Dental Clinic Appointment Manager")

    # Sidebar: FAQ search + general Q&A
    qa_chain = init_faq_qa()
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)

    with st.sidebar:
        st.header("Clinic FAQs")
        faq_q = st.text_input("Search FAQs")
        if faq_q:
            answer = qa_chain.run(faq_q)
            lower = answer.lower()
            if "i don't know" in lower or len(answer.strip()) < 10:
                # if no good FAQ answer, suggest doctor
                answer = "I’m not sure of the answer—please visit your dentist for more details."
            st.markdown(f"**Answer:** {answer}")

        st.markdown("---")
        st.header("General Question")
        gen_q = st.text_input("Ask anything about dental care")
        if gen_q:
            # Use plain LLM to answer any open question
            gen_resp = llm(gen_q)
            st.markdown(f"**Response:** {gen_resp.content}")


    # Date selector for slots
    st.header("Select Date for Appointment")
    selected_date = st.date_input("Choose a date", value=date.today(), min_value=date.today())

    # Fetch slots from DB
    conn  = get_db_conn(DB_CONFIG)
    slots = fetch_upcoming_slots(conn)  # returns dicts with doctor_id, doctor_name, schedule_date, start_time, is_booked
    df    = pd.DataFrame(slots)

    # Filter by selected date
    df['schedule_date'] = pd.to_datetime(df['schedule_date']).dt.date
    df_date = df[df['schedule_date'] == selected_date]

    st.header(f"Available Slots on {selected_date.isoformat()}")
    if df_date.empty:
        st.warning("No slots available for this date.")
    else:
        # Add status and display table
        df_date['Status'] = df_date['is_booked'].map({0: "Open", 1: "Booked"})
        st.table(df_date[['doctor_name','schedule_date','start_time','Status']])

        # Prepare only open slots
        open_df = df_date[df_date['is_booked'] == 0].copy()
        open_df['label'] = open_df.apply(
            lambda r: f"{r['doctor_name']} | {r['schedule_date']} {r['start_time']}", axis=1
        )
        options = open_df['label'].tolist()

        st.header("Book an Appointment")
        with st.form("booking_form", clear_on_submit=True):
            name      = st.text_input("Patient Name")
            address   = st.text_input("Address")
            phone     = st.text_input("Phone Number")
            treatment = st.text_input("Treatment Required")

            if options:
                selected = st.selectbox("Select an open slot", options)
            else:
                st.markdown("**No open slots to select.**")
                selected = None

            submit = st.form_submit_button("Submit")

            if submit:
                if not (name and phone and treatment and selected):
                    st.error("Please fill in all fields and choose a slot.")
                else:
                    # Lookup the row
                    row       = open_df[open_df['label'] == selected].iloc[0]
                    doctor_id = int(row['doctor_id'])
                    time      = str(row['start_time'])

                    success = book_slot(
                        conn,
                        patient_info={'name':name,'address':address,'phone':phone,'treatment':treatment},
                        doctor_id=doctor_id,
                        date=selected_date.isoformat(),
                        time=time
                    )
                    if success:
                        st.success(
                            f"✅ Appointment confirmed for **{name}** on **{selected_date}** at **{time}** "
                            f"with **{row['doctor_name']}**."
                        )
                    else:
                        st.error("❌ That slot was just taken. Please choose another.")

    conn.close()

if __name__ == "__main__":
    main()
