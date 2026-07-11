import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")

print("=" * 60)
print("EVENT REGISTRATION PARSER - Extract Information")
print("=" * 60)

# CHANGED DATA: event registration form instead of a resume
registration = """
Name: Ahmad Raza
Email: ahmad.raza@email.com
Phone: 0300-1234567
City: Lahore
Event: AI Agents & Automation Bootcamp
Ticket Type: Student, Early Bird
Amount Paid: 500 PKR
Registered On: 5th July 2026
"""

print("Registration Text:")
print("-" * 40)
print(registration)
print("-" * 40)

prompt = f"""
Extract information from this event registration form:

{registration}

Return ONLY valid JSON with these keys:
- "name"
- "email"
- "phone"
- "city"
- "event"
- "ticket_type"
- "amount_paid"
- "registered_on"

Do not add any additional text, only return the JSON.
"""

response = model.generate_content(prompt)
print("\nExtracted JSON (Raw Response):")
print(response.text)

# Try to parse the JSON
try:
    # Clean the response if it contains markdown formatting
    cleaned_response = response.text.strip()
    if cleaned_response.startswith('```json'):
        cleaned_response = cleaned_response[7:]
    if cleaned_response.endswith('```'):
        cleaned_response = cleaned_response[:-3]

    parsed_json = json.loads(cleaned_response)

    print("\n" + "=" * 60)
    print("PARSED JSON - Formatted Output")
    print("=" * 60)
    print(json.dumps(parsed_json, indent=2))

    # Display individual fields
    print("\n" + "-" * 40)
    print("EXTRACTED INFORMATION:")
    print("-" * 40)
    for key, value in parsed_json.items():
        print(f"{key}: {value}")

except json.JSONDecodeError as e:
    print(f"\nError parsing JSON: {e}")
    print("Raw response was:")
    print(response.text)

# Bonus: Parse multiple registrations
print("\n" + "=" * 60)
print("BONUS: Parse Multiple Registrations")
print("=" * 60)

registrations = [
    """
    Name: Sara Khan
    Email: sara.khan@email.com
    Phone: 0301-7654321
    City: Karachi
    Event: AI Agents & Automation Bootcamp
    Ticket Type: Professional, Regular
    Amount Paid: 1200 PKR
    Registered On: 6th July 2026
    """,
    """
    Name: Ali Hassan
    Email: ali.hassan@email.com
    Phone: 0302-9876543
    City: Islamabad
    Event: AI Agents & Automation Bootcamp
    Ticket Type: Student, Regular
    Amount Paid: 800 PKR
    Registered On: 7th July 2026
    """
]

for i, registration_text in enumerate(registrations, 1):
    print(f"\nRegistration {i}:")
    print("-" * 30)

    prompt_multiple = f"""
    Extract information from this event registration form:

    {registration_text}

    Return ONLY valid JSON with these keys:
    - "name"
    - "email"
    - "phone"
    - "city"
    - "event"
    - "ticket_type"
    - "amount_paid"
    - "registered_on"

    Do not add any additional text, only return the JSON.
    """

    response = model.generate_content(prompt_multiple)

    try:
        cleaned_response = response.text.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]

        parsed = json.loads(cleaned_response)
        print(f"Name: {parsed.get('name', 'N/A')}")
        print(f"Email: {parsed.get('email', 'N/A')}")
        print(f"Ticket Type: {parsed.get('ticket_type', 'N/A')}")
        print(f"Amount Paid: {parsed.get('amount_paid', 'N/A')}")

    except json.JSONDecodeError:
        print("Error parsing this registration")
        print(f"Raw: {response.text[:100]}...")

print("\n" + "=" * 60)
print("EVENT REGISTRATION PARSING COMPLETE!")
print("=" * 60)