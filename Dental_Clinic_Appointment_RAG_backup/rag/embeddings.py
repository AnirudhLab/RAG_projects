from langchain.embeddings.openai import OpenAIEmbeddings

def get_embeddings(api_key:str):
    return OpenAIEmbeddings(openai_api_key=api_key)
