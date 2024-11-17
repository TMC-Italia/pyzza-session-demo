import requests
import json


def pull_model():
    response = requests.post(
        url="http://ollama_service:11434/api/pull",
        json={"model": "gemma2:2b"}
    )

    if response.status_code == 200:
        msg = "Model Gemma2:2b pulled successfully"
        return msg
    else:
        print(f"Failed to pull model: {response.status_code} - {response.text}")
        return False


def generate_song_with_gemma(input_prompt: str) -> str:
    url = "http://ollama_service:11434/api/generate"
    prompt = f"Generate a christmas song based on the prompt: {input_prompt}"
    payload = {"model": "gemma2:2b", "prompt": prompt}

    response = requests.post(url, json=payload, stream=True)

    if response.status_code == 200:
        response_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    response_text += chunk.get("response", "")
                except json.JSONDecodeError as e:
                    print(f"JSON decoding error: {e}")
        return response_text
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")