# ChatGPT Easy Access 是一个简化访问 ChatGPT 的开源框架。

通过这个框架，您可以轻松地实现以下两个功能：

1. 使用 API Key 进行机器人访问
2. 上传 TXT 文件，创建知识库

# 快速启动
1. 新建api_key.txt，填入自己的openai的API
2. 安装依赖：pip install -r requirements.txt
3. 启动后端：uvicorn backend:app --reload --port 8000
4. 启动前端：streamlit run frontend.py
5. 增加了记忆功能，需要自己开一个mongodb在后台

# TODO

2. 上传 TXT 文件，创建知识库
要创建知识库，请将您的 TXT 文件放在项目的 knowledge_base 文件夹中。确保每个文件包含一个主题，并使用有意义的文件名。例如，如果您有一个关于机器学习的知识库，可以将文件命名为 machine_learning.txt。

接下来，运行以下命令以将这些 TXT 文件转换为知识库：

python create_knowledge_base.py
这将创建一个名为 knowledge_base.json 的文件，其中包含从 TXT 文件中提取的知识库。

要在与 ChatGPT 的对话中使用这些知识库，请运行以下命令：

python chatgpt_bot.py --knowledge_base knowledge_base.json
现在，当与 ChatGPT 进行对话时，它将使用您提供的知识库进行回答。




贡献与支持
我们欢迎您为该项目做出贡献。如果您发现任何问题或有改进意见，请通过提交 issue 或创建 pull request 来参与。

