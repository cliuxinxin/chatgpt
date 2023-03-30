# ChatGPT Easy Access 是一个简化访问 ChatGPT 的开源框架。通过这个框架，您可以轻松地实现以下两个功能：

1. 使用 API Key 进行机器人访问
2. 上传 TXT 文件，创建知识库
# 开始使用

首先，将项目克隆到您的本地计算机上：

git clone https://github.com/yourusername/chatgpt-easy-access.git
cd chatgpt-easy-access

接下来，确保您已经安装了 Python 3.7 或更高版本。然后，安装所需的依赖项：

pip install -r requirements.txt

1. 使用 API Key 进行机器人访问
将您的 ChatGPT API Key 保存在一个名为 api_key.txt 的文件中，将其放在项目的根目录下。

然后，运行以下命令启动与 ChatGPT 的交互：

python chatgpt_bot.py
现在您可以与 ChatGPT 进行实时对话了。

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

