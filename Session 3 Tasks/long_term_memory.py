import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

class MemoryAssistant:
    def __init__(self, storage_file="memory.json"):
        self.storage_file = storage_file
        self.memory_data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}

    def save_memory(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.memory_data, f, indent=2)

    def save_preference(self, user_id, preference):
        if user_id not in self.memory_data:
            self.memory_data[user_id] = []
        self.memory_data[user_id].append({"content": preference})
        self.save_memory()
        return "Preference saved"

    def get_preferences(self, user_id):
        return self.memory_data.get(user_id, [])

    def ask_with_memory(self, user_id, query):
        memories = self.get_preferences(user_id)
        memory_context = "\n".join([m["content"] for m in memories[:5]])

        prompt = f"""
User ID: {user_id}

Previous memories:
{memory_context if memory_context else "No previous data"}

Current question: {query}

Use the memories to give a personalized response.
"""
        response = model.generate_content(prompt)
        return response.text.strip()


assistant = MemoryAssistant()
user_id = "student_001"

print("SESSION 1 - Saving Preferences")
preferences = [
    "My name is Laiba",
    "I like Python programming",
    "My favorite topic is AI",
    "My hobby is coding and reading",
    "My dream job is to be an AI Engineer"
]

for pref in preferences:
    result = assistant.save_preference(user_id, pref)
    print(f"Saved: {pref}")

print("\nSESSION 2 - Retrieving Preferences (New Instance = Simulated Restart)")
new_assistant = MemoryAssistant()

test_queries = [
    "What do I like to learn?",
    "What is my name?",
    "Which programming language do I like?",
    "What is my dream job?"
]

for query in test_queries:
    print(f"You: {query}")
    response = new_assistant.ask_with_memory(user_id, query)
    print(f"Assistant: {response}")