import subprocess  # For executing Python scripts dynamically
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from embeddings.vector_store import retrieve_function, add_function_to_store
from utils.code_generator import generate_execution_code
from memory.session_memory import SessionMemory
import os

# Initialize FastAPI app and session memory
app = FastAPI()
memory = SessionMemory()

# File to store user-defined functions
USER_FUNCTIONS_FILE = "user_defined_func/functions.py"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class QueryRequest(BaseModel):
    prompt: str
    execute: bool = False  # Optional flag to execute the function


@app.post("/execute")
async def execute_function(request: QueryRequest):
    """
    API to process user prompt, retrieve the best function, generate code, 
    and optionally execute it.
    """
    try:
        if not request.prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

        function_name = retrieve_function(request.prompt)

        # If no function found, try using the last executed function from session memory
        if not function_name:
            function_name = memory.get_last_function()
            if not function_name:
                raise HTTPException(status_code=404, detail="Function not found.")

        # Store query in session memory
        memory.add_query(request.prompt, function_name)

        # Generate execution code
        function_code = generate_execution_code(function_name)

        if request.execute:
            try:
                exec(function_code)  # Executes the function dynamically
                logging.info(f"Executed function: {function_name}")
                return {"function": function_name, "code": function_code, "status": "Executed"}
            except Exception as e:
                logging.error(f"Execution error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Error executing function: {str(e)}")

        return {"function": function_name, "code": function_code}

    except HTTPException as he:
        logging.error(f"HTTP Error: {he.detail}")
        raise he  # Re-raise FastAPI HTTP exceptions directly
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")


class UserFunctionRequest(BaseModel):
    name: str
    description: str
    code: str


@app.post("/add_function")
async def add_user_function(request: UserFunctionRequest):
    """Allow users to define new functions dynamically and store them for retrieval."""
    try:
        function_name = request.name.strip()
        function_desc = request.description.strip()
        function_code = request.code.strip()

        if not function_name or not function_code or not function_desc:
            raise HTTPException(status_code=400, detail="Function name, description, and code are required.")

        # Ensure user functions file exists before appending
        if not os.path.exists(USER_FUNCTIONS_FILE):
            try:
                with open(USER_FUNCTIONS_FILE, "w") as f:
                    f.write("# User-defined functions\n")
            except IOError as e:
                logging.error(f"Error creating function file: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to initialize function storage file.")

        # Check for duplicate function names before adding
        try:
            with open(USER_FUNCTIONS_FILE, "r") as f:
                if function_name in f.read():
                    raise HTTPException(status_code=400, detail=f"Function '{function_name}' already exists.")
        except IOError as e:
            logging.error(f"Error reading function file: {str(e)}")
            raise HTTPException(status_code=500, detail="Error accessing stored functions.")

        # Append new function to the file
        try:
            with open(USER_FUNCTIONS_FILE, "a") as f:
                f.write(f"\n\ndef {function_name}():\n")
                for line in function_code.split("\n"):
                    f.write(f"    {line}\n")
        except IOError as e:
            logging.error(f"Error writing function file: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save function definition.")

        logging.info(f"Function '{function_name}' added successfully.")

        # Store function description in FAISS vector store
        try:
            add_function_to_store(function_name, function_desc)
        except Exception as e:
            logging.error(f"Error storing function description: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to store function description.")

        return {
            "message": f"Function '{function_name}' added successfully!",
            "description": function_desc
        }

    except HTTPException as he:
        logging.error(f"HTTP Error: {he.detail}")
        raise he  # Re-raise FastAPI HTTP exceptions directly
    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again.")


