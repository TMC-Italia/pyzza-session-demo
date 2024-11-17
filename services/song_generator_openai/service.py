import os
from openai import OpenAI

# Initialize the OpenAI client
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
if not OPEN_AI_API_KEY:
    raise ValueError("OPEN_AI_API_KEY environment variable is not set.")

client = OpenAI(api_key=OPEN_AI_API_KEY)


def generate_christmas_song(input_prompt: str) -> str:
    prompt = f"Generate a Christmas song based on the prompt: {input_prompt}"

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Choose an appropriate model
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )

    return response.choices[0].text.strip()
