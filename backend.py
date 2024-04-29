import os

from groq import Groq
from dotenv import load_dotenv


class Chatbot:
    def __init__(self):
        load_dotenv()
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY"),
        )
        self.model = "Llama3-8b-8192"
        self.messages = [{
                "role": "system",
                "content": "",
            }]

    def get_response(self, user_input, system_role):
        self.messages[0] = {
            "role": "system",
            "content": system_role,
        }
        self.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )
        if system_role == "":
            sent_messages = self.messages[1:]
        else :
            sent_messages = self.messages

        chat_completion = self.client.chat.completions.create(
            messages=sent_messages,
            model=self.model,
        )
        chat_response = chat_completion.choices[0].message.content
        self.messages.append(
            {
                "role": "assistant",
                "content": chat_response,
            }
        )
        return chat_response

    def reset_conversation(self):
        self.messages = []

    def change_model(self, model):
        self.model = model


if __name__ == "__main__":
    chatbot = Chatbot()
    response = chatbot.get_response("Write a joke about birds.")
    print(response)
