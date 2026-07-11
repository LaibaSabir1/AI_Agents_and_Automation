import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')


class PersonaAgent:
    def __init__(self, role):
        self.role = role
        self.personas = {
            "support": {
                "role": "Professional Customer Support Executive",
                "tone": "Polite, helpful, solution-oriented",
                "style": "Professional and empathetic",
                "constraints": "Always offer solutions, never blame customer"
            },
            "teacher": {
                "role": "Patient University Professor",
                "tone": "Educational, clear, encouraging",
                "style": "Explains concepts with examples",
                "constraints": "No jargon, use simple language, keep it under 100 words"
            },
            "ceo": {
                "role": "Innovative Tech CEO",
                "tone": "Visionary, confident, inspiring",
                "style": "Big picture thinking, strategic",
                "constraints": "Focus on innovation and market impact"
            },
            # --- New personas added for Task 1 ---
            "critic": {
                "role": "Harsh Critic",
                "tone": "Blunt, judgmental, unimpressed",
                "style": "Points out flaws in everything, nitpicks details",
                "constraints": "Never fully praise anything, always find a flaw, keep it under 80 words"
            },
            "creative_writer": {
                "role": "Creative Writer",
                "tone": "Imaginative, expressive, poetic",
                "style": "Responds using stories, metaphors, or poetry",
                "constraints": "Avoid plain/direct answers, wrap the response in a narrative or poetic form"
            }
        }

    def respond(self, question, verbose=True):
        persona = self.personas[self.role]

        if verbose:
            print("\n" + "=" * 50)
            print(f"ROLE: {persona['role']}")
            print(f"TONE: {persona['tone']}")
            print(f"STYLE: {persona['style']}")
            print(f"CONSTRAINTS: {persona['constraints']}")
            print("-" * 50)

        # Create prompt for Gemini with persona
        prompt = f"""
        You are a {persona['role']}.
        Your tone should be: {persona['tone']}
        Your style: {persona['style']}
        Constraints: {persona['constraints']}

        Question: {question}

        Respond to this question in character.
        """

        response = model.generate_content(prompt)

        if verbose:
            print(f"Q: {question}")
            print(f"A: {response.text}")

        return response.text


# RUN DEMO
print("PERSONA PATTERN DEMO - Same Question, Different Personalities")
print("=" * 60)

question = "How do you handle customer complaints?"
roles = ["support", "teacher", "ceo"]

for role in roles:
    agent = PersonaAgent(role)
    agent.respond(question)
    print("-" * 40)

print("\nKEY TAKEAWAY: Persona AI ke responses ko professional aur consistent banata hai!")
print("=" * 60)


# --- Challenge: Compare "Critic" vs "Creative Writer" ---
print("\nCHALLENGE: Critic vs Creative Writer")
print("=" * 60)

challenge_question = "What do you think about pursuing a career in Computer Science?"

critic_agent = PersonaAgent("critic")
creative_agent = PersonaAgent("creative_writer")

critic_response = critic_agent.respond(challenge_question, verbose=False)
creative_response = creative_agent.respond(challenge_question, verbose=False)

print(f"Q: {challenge_question}\n")
print("CRITIC SAYS:")
print(critic_response)
print("\n" + "-" * 40)
print("CREATIVE WRITER SAYS:")
print(creative_response)
print("=" * 60)


# Bonus: Let user choose persona
print("\nBONUS: Choose your own persona!")
print("-" * 40)
all_roles = list(PersonaAgent("support").personas.keys())
print(f"Available personas: {', '.join(all_roles)}")

choice = input("Enter persona name (or 'exit' to quit): ")
if choice in all_roles:
    agent = PersonaAgent(choice)
    custom_question = input("Ask any question: ")
    agent.respond(custom_question)
elif choice != "exit":
    print("Invalid persona selected. Try again!")