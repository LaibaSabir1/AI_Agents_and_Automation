import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

print("=" * 70)
print("SELF-REFINEMENT LOOP")
print("=" * 70)

# STEP 1: Take a topic from the user
topic = input("\nEnter a topic : ")

# STEP 2: AI generates an initial draft
print("\nSTEP 1: Generating Initial Draft...")
print("-" * 70)

draft_prompt = f"""
{topic}

Write it in 3-4 sentences.
"""
draft_response = model.generate_content(draft_prompt)
original_draft = draft_response.text

print("ORIGINAL DRAFT:")
print(original_draft)

# STEP 3: Second call — AI critiques and rewrites its own work
print("\nSTEP 2: Checking Grammar & Marketing Impact, Then Rewriting...")
print("-" * 70)

refine_prompt = f"""
Here is a draft description:

{original_draft}

Check this description for grammar and marketing impact, and rewrite it
to be more persuasive. Fix any grammar issues, strengthen the word choice,
and make it more compelling for a potential buyer.

Give ONLY the final rewritten version, nothing else.
"""
refined_response = model.generate_content(refine_prompt)
refined_draft = refined_response.text

print("REFINED VERSION:")
print(refined_draft)

# STEP 4: Final Step — Print both original and refined outputs side by side
print("\n" + "=" * 70)
print("FINAL COMPARISON: ORIGINAL vs REFINED")
print("=" * 70)

print("\n--- ORIGINAL ---")
print(original_draft)

print("\n--- REFINED (IMPROVED) ---")
print(refined_draft)

print("\n" + "=" * 70)
print("KEY INSIGHT: AI critiqued and improved its own output —")
print("this is the foundation of self-correction / iterative refinement!")
print("=" * 70)