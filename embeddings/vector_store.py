import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
# File to store function metadata
FUNCTION_STORE_FILE = "embeddings/function_store.json"

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_function_data():
    """Load function metadata from JSON file."""
    try:
        with open(FUNCTION_STORE_FILE, "r") as f:
            return json.load(f)  # Load list of function dictionaries
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {str(e)}")

        return []  # Return empty list if file doesn't exist or is corrupted


def save_function_data(function_data):
    """Save function metadata to JSON file."""
    with open(FUNCTION_STORE_FILE, "w") as f:
        json.dump(function_data, f, indent=4)


# Load existing function data on startup
function_data = load_function_data()
print(function_data)

# Convert function descriptions into embeddings
descriptions = [entry["description"] for entry in function_data]
embeddings = embedding_model.encode(descriptions)

# Store in FAISS index
dimension = embeddings.shape[1] 
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))



def add_function_to_store(name, description):
    """Store function description in FAISS and update JSON storage."""
    global function_data

    # Check if function already exists
    if any(func["name"] == name for func in function_data):
        return "Function already exists in vector store."

    # Append new function
    new_function = {"name": name, "description": description}
    function_data.append(new_function)

    # Update FAISS index
    desc_embedding = embedding_model.encode([description])
    index.add(np.array(desc_embedding))

    # Save updated function data
    save_function_data(function_data)

    return f"Stored function '{name}' in vector DB."

def retrieve_function(user_query):
    """Retrieve the best-matching function based on query, with session memory for context."""
    if not function_data:
        return None  # No functions stored yet

    query_embedding = embedding_model.encode([user_query])
    distances, match_idx = index.search(np.array(query_embedding), 1)

    best_match = function_data[match_idx[0][0]]["name"]

    similarity_score = distances[0][0]  # Get similarity score

    print(f"Best Match: {best_match}, Similarity Score: {similarity_score}")  # Debugging

    # Define a threshold for similarity (adjustable)
    SIMILARITY_THRESHOLD = 1.1

    if similarity_score > SIMILARITY_THRESHOLD:
        return False
    
    return best_match


