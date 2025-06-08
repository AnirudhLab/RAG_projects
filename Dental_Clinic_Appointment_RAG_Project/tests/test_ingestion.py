import pytest
from ingestion.pdf_loader import load_and_split

def test_load_and_split():
    chunks = load_and_split('data/clinic_faq.pdf')
    assert len(chunks) > 0
