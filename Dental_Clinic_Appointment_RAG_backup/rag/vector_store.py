from langchain.vectorstores import Chroma

def init_vector_store(docs, embeddings, persist_dir:str):
    vs = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    vs.persist()
    return vs
