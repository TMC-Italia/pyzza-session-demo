import ollama


def perform_task(prompt: str):
    # Use OpenAI's API to generate a song or text based on the prompt
    # client = OpenAI(
    #    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    # )

    # chat_completion = client.chat.completions.create(
    #    messages=[
    #        {
    #            "role": "user",
    #            "content": "Say this is a test",
    #        }
    #    ],
    #    model="gpt-4",
    # )
    # TODO custom prompt
    response = ollama.generate(
        model='gemma2:2b', prompt='genera una canzone natalizia in italiano'
    )
    if answer := response.get('response'):
        return answer
    raise 'Got no answer from model'
    # return chat_completion.choices[0].message.content
