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
        raise ValueError(f"Function '{function_name}' not found in automated or user-defined functions. soo")

    template = f"""
import sys
import importlib

# Dynamically import the module
module = importlib.import_module("{module_path}")

def main():
    try:
        result = getattr(module, "{function_name}")()
        print(f"Function executed successfully: {{result}}" if result else "Function executed.")
    except Exception as e:
        print(f"Error executing function: {{e}}")

if __name__ == "__main__":
    main()
    """

    return template

