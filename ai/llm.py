from groq import Groq
import os
from dotenv import load_dotenv


load_dotenv()


class LLM:
    def __init__(self, system_prompt="You are a helpful assistant."):
        self.client = Groq(
            api_key=os.getenv("GROQ_API"),
        )
        self.model = "llama-3.3-70b-versatile"
        self.system_prompt = system_prompt

    def query(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        response = chat_completion.choices[0].message.content
        return response

