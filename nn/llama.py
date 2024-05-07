import ollama


def reply(messages: list):
    response = ollama.chat(model='llama3', messages=messages)
    return response['message']
