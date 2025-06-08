import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'dental_clinic')
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FAQ_PDF_PATH = os.getenv('FAQ_PDF_PATH', 'data/clinic_faq.pdf')
VECTORSTORE_DIR = os.getenv('VECTORSTORE_DIR', 'vectorstore')
