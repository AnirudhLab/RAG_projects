from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

class AppointmentAgent:
    def __init__(self, vector_store, sql_store, llm_key):
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(openai_api_key=llm_key, temperature=0),
            chain_type='stuff',
            retriever=vector_store.as_retriever()
        )
