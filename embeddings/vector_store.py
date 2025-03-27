import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Define function metadata
function_data = [
    ("open_chrome", "Opens Google Chrome browser"),
    ("open_calculator", "Launches the system calculator"),
    ("get_cpu_usage", "Fetches the current CPU usage"),
    ("get_ram_usage", "Retrieves RAM usage details"),
]

# Convert function descriptions into embeddings
descriptions = [desc for _, desc in function_data]
embeddings = embedding_model.encode(descriptions)

# Store in FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def add_function_to_store(name, description):
    """Store function description in FAISS, avoiding duplicates."""
    for stored_name, _ in function_data:
        if stored_name == name:
            return "Function already exists in vector store."
    
    function_data.append((name, description))
    desc_embedding = embedding_model.encode([description])
    index.add(np.array(desc_embedding))
    return f"Stored function '{name}' in vector DB."

def retrieve_function(user_query):
    """Retrieve the best-matching function based on query."""
    if not function_data:
        return None  # No functions stored yet
    
    query_embedding = embedding_model.encode([user_query])
    _, match_idx = index.search(np.array(query_embedding), 1)
    
    return function_data[match_idx[0][0]][0]  # Return function name

