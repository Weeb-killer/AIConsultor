from zhipuai import ZhipuAI
import yaml

CONFIG_FILE = 'config.yaml'

with open(CONFIG_FILE, 'r') as config_file:
    config = yaml.load(config_file)

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
        prompt=messages
    )
    try:
        answer = response.choices[0].message.content
    except:
        answer = "System Error."
    pass
    return "answer"


# def output():
#     while True:
#         user_input = input()
#         if user_input.lower() in ['exit', 'quit']:
#             print("Exit. Goodbye!")
#             break
#         response = get_chatgpt_response(user_input)
#         print("ChatGPT: " + response)
