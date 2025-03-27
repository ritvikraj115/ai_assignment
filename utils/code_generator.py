import importlib
import automation_functions.functions as auto_funcs

def generate_execution_code(function_name):
    import user_defined_func.functions as user_funcs
    
    """Generate a Python script to invoke the retrieved function from the correct module."""

    # Check if function exists in automated functions
    if hasattr(auto_funcs, function_name):
        module_path = "automation_functions.functions"
    elif hasattr(user_funcs, function_name):
        module_path = "user_defined_func.functions"
    else:
        raise ValueError(f"Function '{function_name}' not found in automated or user-defined functions.")

    # Properly formatted execution script
    template = f"""import sys
import importlib

def main():
    try:
        # Dynamically import the module
        module = importlib.import_module("{module_path}")
        
        # Get and execute the function
        func = getattr(module, "{function_name}")
        result = func()
        
        if result:
            print(f"Function executed successfully: {{result}}")
        else:
            print("Function executed.")
    
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
"""

    return template
