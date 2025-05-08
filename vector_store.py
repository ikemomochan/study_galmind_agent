# vector_store.py

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv()

# 保存先ディレクトリ
VECTOR_DIR = "vectorstore"
os.makedirs(VECTOR_DIR, exist_ok=True)

# OpenAI埋め込みモデルの準備
embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# FAISS保存関数
def save_to_vectorstore(texts: list[str], metadatas: list[dict], index_name: str):
    documents = [Document(page_content=t, metadata=m) for t, m in zip(texts, metadatas)]
    vectorstore = FAISS.from_documents(documents, embedding_model)
    path = os.path.join(VECTOR_DIR, index_name)
    vectorstore.save_local(path)
    print(f"💾 FAISSに保存したよ〜！ {path}")

# FAISS読み込み関数
def load_vectorstore(index_name: str):
    path = os.path.join(VECTOR_DIR, index_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"まだ保存されてないみたい💦: {index_name}")
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
