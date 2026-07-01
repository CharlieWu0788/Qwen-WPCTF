from openai import OpenAI


class LLMClient:
    def __init__(self, base_url="http://127.0.0.1:1234/v1", model="meta-llama-3.1-8b-instruct-abliterated"):
        self.base_url = base_url
        self.model = model

        self.client = OpenAI(
            base_url=self.base_url,
            api_key="lm-studio"
        )

    def chat(self, prompt: str, temperature=0):
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional cybersecurity analyst. Always follow the user's output format exactly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()