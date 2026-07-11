import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-flash-latest')

print("=" * 70)
print("TRAVEL PLANNER AGENT - Flipped Interaction")
print("=" * 70)

questions = [
    "What destination would you like to travel to?",
    "What is your budget for this trip?",
    "How many days will your trip be?"
]

answers = {}
print("\nAI: Hi! I'm your Travel Planner. I'll ask you 3 quick questions "
      "to build your itinerary.\n")

# STEP 1: Ask exactly three questions, ONE AT A TIME
for i, question in enumerate(questions, start=1):
    print(f"AI: {question}")
    user_answer = input("You: ")
    answers[question] = user_answer
    print()  # spacing, waits for response before asking next question

# STEP 2: Once all three are answered, generate the Travel Itinerary
print("=" * 70)
print("GENERATING YOUR TRAVEL ITINERARY...")
print("=" * 70)

itinerary_prompt = f"""
You are a professional travel planner. Based on the following details
the user provided, create a comprehensive and practical travel itinerary.

Destination: {answers[questions[0]]}
Budget: {answers[questions[1]]}
Number of Days: {answers[questions[2]]}

Create a detailed day-by-day itinerary including:
1. A short trip overview
2. Suggested accommodation type (within the given budget)
3. Day-by-day activities and sightseeing plan
4. Estimated cost breakdown (travel, stay, food, activities)
5. Local food recommendations
6. A few practical travel tips for this destination

Keep it realistic and tailored to the stated budget and duration.
"""

response = model.generate_content(itinerary_prompt)

print("\nYOUR TRAVEL ITINERARY:")
print("-" * 70)
print(response.text)
print("-" * 70)

print("\nKEY TAKEAWAY: The AI waited for the user's response after EACH")
print("question instead of asking all three at once — this is the")
print("'Flipped Interaction' / clarification pattern!")
print("=" * 70)