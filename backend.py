import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pymongo
from pymongo import MongoClient
import faiss
import numpy as np

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    knowledge_base: Optional[str] = None

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
conversations_collection = db["conversations"]

# 创建 Faiss 索引
dimension = 1536  # 请根据实际使用的模型设置相应的维度
index_flat_l2 = faiss.IndexFlatL2(dimension)
faiss_index = faiss.IndexIDMap(index_flat_l2)

def get_api_key():
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()
    return api_key

openai.api_key = get_api_key()

def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input=[text], model=model)
    return response['data'][0]['embedding'] # 1536

def store_conversation(text, embedding):
    conversation_id = conversations_collection.count_documents({})
    conversation = {
        "_id": conversation_id,
        "text": text,
        "embedding": embedding
    }
    result = conversations_collection.insert_one(conversation)
    faiss_index.add_with_ids(np.array([embedding]), np.array([conversation_id], dtype=np.int64))
    return result

def find_most_similar_conversation(query_embedding, k=2):
    distances, indices = faiss_index.search(np.array([query_embedding]), k)
    similar_conversations = []
    for index in indices[0]:
        conversation = conversations_collection.find_one({"_id": int(index)})
        similar_conversations.append(conversation)
    return similar_conversations

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

    # 对每个用户和AI发送的消息进行嵌入计算并保存到数据库中
    for message in chat_request.messages:
        embedding = get_embedding(message.content)
        store_conversation(message.content, embedding)

    # 使用 Faiss 索引查询与当前消息相似的消息
    current_message_embedding = get_embedding(chat_request.messages[-1].content)
    similar_conversations = find_most_similar_conversation(current_message_embedding)

    # 将找到的相似消息作为背景知识传递给聊天函数
    knowledge_base = " ".join([conv["text"] for conv in similar_conversations])

    # 创建一个只包含本次用户提问和背景知识的新消息列表
    new_messages = [Message(role="system", content=knowledge_base), chat_request.messages[-1]]
                    
    response = chat(new_messages, knowledge_base)
    print(f"Generated response: {response}")  # Debug output

    # 将AI生成的响应及其嵌入保存到数据库中
    response_embedding = get_embedding(response)
    store_conversation(response, response_embedding)

    return {"response": response}
