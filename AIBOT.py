from openai import OpenAI

client = OpenAI(api_key="...")


def get_chatgpt_response(prompt):
    # messages = []
    # messages.append({"role": "system", "content": "You are a chatbot."})
    # messages.append({"role": "assistant", "content": ""})
    #
    # user_question = {}
    # user_question['role'] = 'user'
    # user_question['content'] = prompt
    #
    # messages.append(user_question)
    #
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages
    # )
    # try:
    #     answer = response.choices[0].message.content
    # except:
    #     answer = "System Error."
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
