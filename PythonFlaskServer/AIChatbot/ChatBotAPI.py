from google import genai
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

GenAI_API_KEY = os.getenv("GENAI_API_KEY")

MAX_REQUESTS_PER_MINUTE = 15
usage_counter = 0
start_time = time.time()

client = genai.Client(api_key=GenAI_API_KEY)

def chatBotResponse(prompt):
    global usage_counter, start_time
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time < 60:
        if usage_counter >= MAX_REQUESTS_PER_MINUTE - 5:  # 5 requests left
            print("You are approaching the maximum number of requests per minute.")
            return
    else:
        start_time = current_time
        usage_counter = 0
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        {
            "role": "user",
            "parts": [{
                "text": "You are a traffic prediction assistant designed to provide accurate and helpful information about traffic conditions between two locations. Your predictions are based on historical traffic data, real-time trends, and other relevant factors. Your tasks include predicting traffic conditions between two locations based on historical data, providing estimated travel times during specific times such as rush hour, suggesting alternative routes if traffic conditions are expected to be poor, and answering questions about traffic patterns, peak hours, and road conditions. When responding, be concise and clear. Provide estimates with a confidence level, for example, 'Based on historical data, there is a 70% chance of heavy traffic during rush hour.' If you don't have enough data to make a prediction, say so and suggest other resources."
            }]
        },
        {
            "role": "user",
            "parts": [{"text": prompt}]
        }
    ]
)
    usage_counter += 1
    return response.text

# Don't need this in production, the prompt will come from the web request
def main():
    print("Welcome to the OpenAI Chatbot! Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break

        response = chatBotResponse(user_input)
        print(f"Chatbot: {response}")
        print("Welcome to the OpenAI Chatbot! Type 'exit' to end the conversation.")

if __name__ == "__main__":
    main()
