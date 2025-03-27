import re
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
    def is_ambiguous(self,user_query):
        """Check if the user's query is vague and lacks specific context."""
        vague_patterns = [
            r"\b(it|that|this|same|again|previous|last|repeat|continue|do the same|follow up)\b",
            r"\b(as before|like before|similar to last|similar to previous)\b",
            r"\b(just like|same as|like that|like this)\b",
            r"\b(use previous|refer last|repeat last action|redo it)\b",
            r"\b(keep going|carry on|maintain same|keep same)\b"
        ]
        
        query_lower = user_query.lower()
        for pattern in vague_patterns:
            if re.search(pattern, query_lower):
                return True  # Query is ambiguous
        
        return False  # Query is clear

