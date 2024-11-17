import json
import requests



def pull_model():
    response = requests.post(
        url="http://ollama_service:11434/api/pull",
        json={"model": "gemma2:2b"}
    )

    if response.status_code == 200:
        print("Model pulled successfully.")
        return True
    print(f"Failed to pull model: {response.status_code} - {response.text}")
    return False


def generate_song_with_gemma(input_prompt: str) -> str:
    url = "http://ollama_service:11434/api/generate"
    prompt = f"Generate a christmas song based on the prompt: {input_prompt}"
    payload = {"model": "gemma2:2b", "prompt": prompt, 'stream': False}

    response = requests.post(url, json=payload, stream=False)
    try:
        response_json = json.loads(response.content)
        return response_json["response"]
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
