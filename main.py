# This is a sample Python script.
import json
import string

import openai

from functions import DatetimeFunction, SystemFunction

# Press Maiusc+F10 to execute it or replace it with your code.

with open("cfg.json") as f:
    configs = json.load(f)
    api_key = configs["api_key"]
    prompt = configs["prompt"]
    isEnabledSysFunc = configs["system_function_enabled"]

messages = []
functions = []
role_system = "system"
role_user = "user"
role_assistant = "assistant"
role_function = "function"
openai.api_key = api_key


def addFunction(function):
    functions.append(function.descriptor())


def addFunctionMessage(function_name: string, function_response: string):
    messages.append({"role": role_function, "name": function_name, "content": function_response})


def addUserMessage(usr_input):
    messages.append({"role": role_user, "content": usr_input})


def addSystemMessage(sys_input):
    messages.append({"role": role_system, "content": sys_input})


def addAssistantMessage(ass_input):
    messages.append({"role": role_assistant, "content": ass_input})


def function_call(ai_message):
    if ai_message.get("function_call"):
        available_functions = {
            "datetime_function": DatetimeFunction.execute,
            "system_function": SystemFunction.execute
        }
        function_name = ai_message["function_call"]["name"]
        if function_name not in available_functions:
            print(f'Function {function_name} not found.')
            return
        function_to_call = available_functions[function_name]
        parameters = json.loads(ai_message["function_call"]["arguments"])
        function_response = function_to_call(parameters=parameters)
        addFunctionMessage(function_name, function_response)
        addOpenaiMessage()
    else:
        addAssistantMessage(ai_message["content"])


def addOpenaiMessage():
    while True:
        try:
            rs = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                functions=functions,
                function_call="auto",
                temperature=0.5
            )
            function_call(rs.choices[0]['message'])
            return
        except openai.error.InvalidRequestError as error:
            if 'maximum context length' in str(error):
                del messages[:len(messages) // 3]  # remove the oldest messages
            else:
                raise


if __name__ == '__main__':
    addSystemMessage(prompt)
    addFunction(DatetimeFunction())
    if isEnabledSysFunc:
        addFunction(SystemFunction())
    print(f'Starting AI interaction with prompt:\n{prompt}')
    try:
        while True:
            user_input = input("\nHUMAN: ")
            addUserMessage(user_input)
            addOpenaiMessage()
            print(f"\nOPEN-AI: {messages[-1]['content']}")
    except KeyboardInterrupt:
        print("Interaction with openAI finished")
