import re
class Agent:
    def __init__(self):

        # 4 Main Components
        self.persona = "Friendly Customer Support"
        self.memory = []  # Learning
        self.tools = {    # Capabilities
            "check_order": self.check_order,
            "refund": self.process_refund,
            "calculate": self.calculate   # NEW TOOL
        }
        self.knowledge = {
            "policy": "30-day refund policy",
            "hours": "9 AM - 6 PM"
        }
    # TOOLS
    def check_order(self, order_id):
        return f"Order #{order_id}: Shipped, arriving tomorrow"

    def process_refund(self, order_id):
        return f"Refund #{order_id}: Approved, money back in 5 days"
    # NEW TOOL: Basic Math (Addition/Subtraction)
    def calculate(self, expression):
        num1, operator, num2 = expression
        if operator == "add":
            result = num1 + num2
            return f"Calculation: {num1} + {num2} = {result}"
        elif operator == "subtract":
            result = num1 - num2
            return f"Calculation: {num1} - {num2} = {result}"
        else:
            return "Sorry, I can only add or subtract right now."

    # Helper: Extract numbers and operation from user input
    def extract_math(self, user_input):
        numbers = [int(n) for n in re.findall(r'\d+', user_input)]
        if len(numbers) >= 2:
            if "add" in user_input.lower() or "plus" in user_input.lower() or "+" in user_input:
                return (numbers[0], "add", numbers[1])
            elif "subtract" in user_input.lower() or "minus" in user_input.lower() or "-" in user_input:
                return (numbers[0], "subtract", numbers[1])
        return None

    # AGENT LOOP
    def process(self, user_input):
        print("." * 50)
        print(" AGENT LOOP IN ACTION")
        print("." * 50)

        # PERCEIVE (What user said)
        print(f"\n PERCEIVE: User → '{user_input}'")
        self.memory.append({"user": user_input})

        # PROCESS (Think with brain)
        print(f" PROCESS: Analyzing...")
        math_data = self.extract_math(user_input)

        if math_data:
            action = "calculate"
        elif "order" in user_input.lower():
            action = "check_order"
        elif "refund" in user_input.lower():
            action = "refund"
        else:
            action = "respond"

        # DECIDE (Choose action)
        print(f" DECIDE: Action selected → {action}")

        # ACT (Execute)
        print(f" ACT: Executing...")
        if action == "calculate":
            result = self.tools["calculate"](math_data)
        elif action in self.tools:
            result = self.tools[action]("123")
        else:
            result = f"Hi! I can help with orders, refunds, or calculations. {self.knowledge['policy']}"

        print(f" Result: {result}")
        self.memory.append({"agent": result})

        print(f"\n Memory: {len(self.memory)} interactions")
        return result


# RUN DEMO
agent = Agent()
print("\n Agent Starting...\n")
queries = ["Check my order", "I want refund", "Add 50 and 20", "Subtract 30 from 100", "Hello"]
for q in queries:
    agent.process(q)
    print("." * 40)

print("\n KEY TAKEAWAY: Har Agent yehi loop follow karta hai!")
# Interactive mode - user khud type kar sakta hai
print("\n" + "=" * 50)
print("Ab aap khud test karein! (type 'exit' to quit)")
print("=" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    agent.process(user_input)