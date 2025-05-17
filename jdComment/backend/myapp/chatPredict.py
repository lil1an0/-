from openai import OpenAI

client =OpenAI(api_key="sk-bcbbe2308fc843868e65202249109a2e", base_url="https://api.deepseek.com")

def sentiment_predict(content):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个人类的朋友，对该评论做一个情感分类，用两个字来打个标签就可以, 从 好评、中评、差评 中选一个"},
            {"role": "user", "content": content}
        ],
        stream=False
    )
    return response.choices[0].message.content