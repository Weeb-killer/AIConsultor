from zhipuai import ZhipuAI
import yaml

CONFIG_FILE = 'config.yaml'

with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.load(config_file,Loader=yaml.FullLoader)

model = "glm-4-0520"
client = ZhipuAI(api_key=config['zhipuai']['api_key'])



def get_zhipuai_response(prompt):
    messages = []
    messages.append({"role": "system", "content": "You are a chatbot."})
    messages.append({"role": "assistant", "content": ""})

    user_question = {}
    user_question['role'] = 'user'
    user_question['content'] = prompt

    messages.append(user_question)

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    try:
        answer = response.choices[0].message.content
    except:
        answer = "System Error."

    return answer

