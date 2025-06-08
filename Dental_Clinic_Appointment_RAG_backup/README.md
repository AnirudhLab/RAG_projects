# Dental RAG Appointment Manager

This project provides a Streamlit-based RAG system for managing dental clinic appointments, combining a PDF-based FAQ retrieval with MySQL-backed scheduling.

## Structure
- **app/**: Streamlit UI and config
- **ingestion/**: PDF loading and schedule fetching
- **rag/**: embeddings, vector store, SQL wrappers, and agent
- **tests/**: pytest files

## Setup
1. Copy `.env.sample` → `.env` and fill in DB & OpenAI credentials.
2. `pip install -r requirements.txt`
3. Initialize MySQL schema with doctors & schedule.
4. Place `clinic_faq.pdf` in `data/`.
5. `streamlit run app/main.py`
