import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# ---- The 3 problems given in the assignment ----
problems = [
    "What is 15% of 200?",
    "If 5 apples cost 50 rupees, what do 8 apples cost?",
    "A square has side 6 cm. What is its area?",
]


def ask_without_cot(question):
    """Direct answer, no reasoning requested"""
    response = model.generate_content(question)
    return response.text.strip()


def ask_with_cot(question):
    """Same question + CoT trigger phrase"""
    cot_prompt = question + "\n\nLet's think step by step and show all calculations."
    response = model.generate_content(cot_prompt)
    return response.text.strip()


results = []

for i, problem in enumerate(problems, 1):
    print("=" * 70)
    print(f"PROBLEM {i}: {problem}")
    print("=" * 70)

    print("\n[WITHOUT CoT]")
    answer_no_cot = ask_without_cot(problem)
    print(answer_no_cot)

    print("\n[WITH CoT]")
    answer_cot = ask_with_cot(problem)
    print(answer_cot)

    print("-" * 70 + "\n")

    results.append(
        {
            "problem": problem,
            "without_cot": answer_no_cot,
            "with_cot": answer_cot,
        }
    )

# Simple summary table at the end
print("=" * 70)
print("SUMMARY")
print("=" * 70)
for r in results:
    print(f"\nProblem: {r['problem']}")
    print(f"  Without CoT -> {r['without_cot'][:80]}...")
    print(f"  With CoT    -> {r['with_cot'][:80]}...")