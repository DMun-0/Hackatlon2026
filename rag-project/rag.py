import langchain
from langchain_community.llms import Ollama
from langchain.document_loaders import TextLoader

from langchain.text_splitters import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# -------------------------
# 1. Last dokument
# -------------------------
loader = TextLoader("dokuments/syn-på-ki.txt")  # pass på riktig filsti
documents = loader.load()

# -------------------------
# 2. Del opp tekst
# -------------------------
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# -------------------------
# 3. Lag embeddings
# -------------------------
embeddings = HuggingFaceEmbeddings()

# -------------------------
# 4. Lag vektordatabase
# -------------------------
db = Chroma.from_documents(texts, embeddings)

# -------------------------
# 5. Koble til Ollama
# -------------------------
llm = Ollama(model="llama3")  # Husk å starte Ollama i egen terminal!

# -------------------------
# 6. Spørsmål + retrieval
# -------------------------
query = "Hva handler dokumentet om?"
docs = db.similarity_search(query)

# Sett sammen kontekst
context = "\n".join([doc.page_content for doc in docs])

# Lag prompt til LLM
prompt = f"""
Svar på spørsmålet basert på kontekst:

Kontekst:
{context}

Spørsmål:
{query}
"""

# -------------------------
# 7. Få svar fra LLM
# -------------------------
response = llm.invoke(prompt)
print("Svar fra Ollama:\n")
print(response)
