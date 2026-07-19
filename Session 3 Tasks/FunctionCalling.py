import google.generativeai as genai
import re

# STEP 1: Configure Gemini API - step 1

from dotenv import load_dotenv
load_dotenv()
import os
key = os.environ.get("GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-flash-latest")

# Define the weather function - step 2

def get_weather(city: str) -> str:
    """Returns mock weather data for a given city"""
    weather_data = {
        "paris": "Cloudy, 18°C, light rain",
        "london": "Foggy, 12°C, light drizzle",
        "karachi": "Hot and humid, 35°C, clear sky",
        "tokyo": "Sunny, 25°C, light breeze",
        "lahore": "Smoggy, 30°C, moderate pollution",
        "dubai": "Sunny, 42°C, extreme heat",
        "new york": "Partly cloudy, 22°C, windy",
        "sydney": "Sunny, 28°C, mild breeze"
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        return f"{city}: {weather_data[city_lower]}"
    else:
        return f"{city}: Weather data not available"

# The Agent - Main logic - step 3 (SINGLE Gemini call per query)

def run_agent(user_query: str):
    """Main agent that processes user query using Gemini function calling.
    Only ONE call to generate_content() per query — the friendly final
    reply is built locally in Python instead of asking Gemini again."""

    print(f"\n User: {user_query}")

    prompt = f"""
You are a weather assistant. You have access to the following function:

Function: get_weather(city: str) -> str
Description: Returns weather information for a given city.

If the user asks about weather in any city, you MUST call the get_weather function with the city name.
If the user asks something else, just reply normally.

User query: {user_query}

IMPORTANT:
- If weather is asked, respond ONLY with: FUNCTION_CALL: get_weather(city="city_name")
- Replace city_name with the actual city from the query
- If no weather is asked, respond normally
"""

    # Single API call
    response = model.generate_content(prompt)
    response_text = response.text.strip()

    if "FUNCTION_CALL:" in response_text:
        print(" Agent: I need to call the weather function...")
        try:
            function_call_part = response_text.split("FUNCTION_CALL:")[1].strip()

            if "get_weather" in function_call_part:
                match = re.search(r'city=["\']([^"\']+)["\']', function_call_part)
                if match:
                    city = match.group(1)
                    print(f" Function Called: get_weather(city='{city}')")

                    # Call the actual function
                    weather_result = get_weather(city)

                    # Build the friendly reply locally — NO second API call
                    friendly_reply = f"Here's the latest for {city.title()}: {weather_result.split(': ', 1)[1]}."
                    print(f" Assistant: {friendly_reply}")
                else:
                    print(" Assistant: Could not find city in function call.")
            else:
                print(f" Assistant: {response_text}")

        except Exception as e:
            print(f" Assistant: Error - {str(e)}")
            print(f"Raw response: {response_text}")
    else:
        # No function call needed
        print(f" Assistant: {response_text}")

# Test the Agent - step 4

if __name__ == "__main__":
    print("=" * 60)
    print("  WEATHER REPORT ASSISTANT")
    print("=" * 60)

    test_queries = [
        "Paris ka mausam kaisa hai?",
        "What's the weather in London?",
        "Tell me about Karachi weather",
        "How's the temperature in Tokyo?",
        "Hello, how are you?",
        "Is it hot in Dubai?"
    ]

    for query in test_queries:
        run_agent(query)
        print("-" * 50)

    # Interactive mode
    print("\n Type your query (or 'exit' to quit):")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            break
        run_agent(user_input)