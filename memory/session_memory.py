class SessionMemory:
    """Simple session memory to store past user interactions."""
    def __init__(self):
        self.history = []

    def add_query(self, query, function_name):
        """Store user query and matched function."""
        self.history.append({"query": query, "function": function_name})

    def get_last_function(self):
        """Retrieve the last executed function."""
        return self.history[-1]["function"] if self.history else None
