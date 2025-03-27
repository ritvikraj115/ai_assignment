# LLM + RAG-Based Function Execution API

## Overview
This project implements an API that dynamically retrieves and executes automation functions using LLM + RAG (Retrieval-Augmented Generation).

## Features
✅ Function registry with predefined automation functions  
✅ Retrieval-Augmented Generation (RAG) using FAISS for function retrieval  
✅ Dynamic Python script generation for function invocation  
✅ Persistent session memory for context-aware execution  
✅ REST API built using FastAPI  
✅ Persistent storage of user-defined functions  
✅ Supports shell command execution and system monitoring utilities  

## Installation

### 1. Clone the Repository
```sh
git clone https://github.com/ritvikraj115/ai_assignment.git
cd ai-assignment
```

### 2. Create and Activate Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Run the FastAPI Server
```sh
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### 1. Execute Function
- **Endpoint:** `POST /execute`
- **Description:** Retrieves the best-matching function based on user query, generates code, and optionally executes it.
- **Request Body (JSON):**
  ```json
  {
    "prompt": "get cpu usage",
  }
  ```
- **Response (JSON):**
  ```json
  {
    "function": "get_cpu_usage",
    "code": "def get_cpu_usage(): return psutil.cpu_percent()",
  }
  ```

### 2. Add a New Function
- **Endpoint:** `POST /add_function`
- **Description:** Allows users to define new automation functions that are permanently stored.
- **Request Body (JSON):**
  ```json
  {
    "name": "greet",
    "description": "Returns a greeting message",
    "code": "def greet(): return 'Hello, user!'"
  }
  ```
- **Response (JSON):**
  ```json
  {
  "message": "Function 'greet' added successfully!",
  "description": "Returns a greeting message"
}
  ```

## Notes
- User-defined functions persist even after server restarts.
- Uses FAISS to find the most relevant function based on vector embeddings.
- Supports session memory to retain context for better function execution.

---

