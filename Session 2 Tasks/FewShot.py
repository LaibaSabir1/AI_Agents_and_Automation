import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-flash-latest')

print("=" * 70)
print(" FEW-SHOT PROMPTING - Poetic Urdu Book Titles")
print("=" * 70)

# FEW-SHOT PROMPT with examples
few_shot_prompt = """
Translate these book titles into a poetic, emotional Urdu style:

Pride and Prejudice -> Ghuroor aur Ghalatfehmi ka Qissa.
The Alchemist -> Manzil ki Talaash mein Ek Rooh.
Wuthering Heights -> Toofano mein Basi Mohabbat.
The Kite Runner -> Guzray Waqt ka Karz.
Norwegian Wood -> Bhoole Bisre Jungle ki Yaadein.

Now translate these books using the SAME poetic style:
1. To Kill a Mockingbird
2. The Great Gatsby
3. 1984
4. Little Women
5. The Book Thief

Rules:
- Keep it emotional and poetic, not funny
- Use simple Urdu/Urdu mixed with English
- Be creative but follow the pattern
"""

response = model.generate_content(few_shot_prompt)

print("\n AI's Response:")
print("-" * 70)
print(response.text)
print("-" * 70)

print("\n KEY INSIGHT:")
print("Same few-shot technique as the original (funny movie titles),")
print("just swapped the domain and tone (books, poetic instead of funny).")
print("The model still learned the STYLE purely from the 5 examples given,")
print("with zero fine-tuning - proving few-shot prompting generalizes to")
print("any content type as long as the pattern in the examples is clear.")