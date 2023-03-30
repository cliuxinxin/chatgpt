import openai
import pymongo
from pymongo import MongoClient
import faiss
import numpy as np

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

# 存储对话的函数
def store_conversation(text, embedding):
    # 获取当前文档数量作为整数ID
    conversation_id = conversations_collection.count_documents({})

    conversation = {
        "_id": conversation_id,
        "text": text,
        "embedding": embedding.tolist()
    }
    # 将对话存储到 MongoDB
    result = conversations_collection.insert_one(conversation)
    
    # 将 embedding 添加到 Faiss 索引
    faiss_index.add_with_ids(np.array([embedding]), np.array([conversation_id], dtype=np.int64))
    
    return result



# 查找最相关对话的函数
def find_most_similar_conversation(query_embedding, k=2):
    # 使用 Faiss 索引查询最相似的 embedding
    distances, indices = faiss_index.search(np.array([query_embedding]), k)
    
    # 从 MongoDB 中获取对应的对话
    similar_conversations = []
    for index in indices[0]:
        conversation = conversations_collection.find_one({"_id": int(index)})  # 将 index 转换为 int 类型
        similar_conversations.append(conversation)
    
    return similar_conversations



# # 使用方法
# text = "天下第一的武功是什么？"
# embedding = get_embedding(text)
# print(embedding)

# 示例：存储对话
user_id = 1
text = "汉堡的首都在哪里"
embedding = np.random.rand(dimension)  # 示例使用随机向量，实际情况下请使用 get_embedding 函数获取 embedding
result = store_conversation(text, embedding)

# 示例：查找最相关对话
query_embedding = np.random.rand(dimension)  # 示例使用随机向量，实际情况下请使用 get_embedding 函数获取 embedding
similar_conversations = find_most_similar_conversation(query_embedding)
print(similar_conversations)
