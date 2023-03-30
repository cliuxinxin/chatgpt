import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    knowledge_base: Optional[str] = None

def get_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

openai.api_key = get_api_key()

def chat(messages, knowledge_base=None):
    messages_dicts = [message.dict() for message in messages] 

    if knowledge_base:
        messages.insert(0, {"role": "system", "content": f"{knowledge_base}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_dicts
    )

    return response.choices[0].message.content.strip()

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    print(f"Received request: {chat_request}")  # Debug output
    response = chat(chat_request.messages, chat_request.knowledge_base)
    print(f"Generated response: {response}")  # Debug output
    return {"response": response}

