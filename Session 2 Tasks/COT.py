import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Model
model = genai.GenerativeModel("gemini-flash-latest")

# Problems
problems = [
    "What is 15% of 200?",
    "If 5 apples cost 50 rupees, what do 8 apples cost?",
    "A square has side 6 cm. What is its area?"
]

print("=" * 60)
print("TASK 1: Practice Different Problems")
print("=" * 60)

for i, problem in enumerate(problems, start=1):

    print(f"\nProblem {i}: {problem}")

    # Without CoT
    print("\nWITHOUT CoT:")
    response1 = model.generate_content(
        f"Answer the following question directly:\n{problem}"
    )
    print(response1.text)

    # With CoT
    print("\nWITH CoT:")
    response2 = model.generate_content(
        f"Solve the following problem step by step:\n{problem}"
    )
    print(response2.text)

    print("-" * 60)

print("\n" + "=" * 60)
print("OBSERVATIONS")
print("=" * 60)

print("""
1. Problem 1 (15% of 200)
   - Without CoT: 30
   - With CoT: Shows percentage calculation and gives 30.
   - Better Answer: With CoT (clear explanation).

2. Problem 2 (5 apples cost 50 rupees)
   - Without CoT: 80 rupees
   - With CoT: Calculates price per apple (10 rupees) and then 8 × 10 = 80.
   - Better Answer: With CoT.

3. Problem 3 (Square side = 6 cm)
   - Without CoT: 36 cm²
   - With CoT: Uses Area = side × side = 6 × 6 = 36 cm².
   - Better Answer: With CoT.

Questions:
1. For each problem, which answer was better?
   -> The With CoT answers were better because they explained the calculation.

2. Did CoT help in every problem?
   -> Yes. It made the reasoning easier to understand and verify.

3. Which type of problem was CoT most useful for?
   -> Problem 2 (the word problem involving proportional reasoning).
""")