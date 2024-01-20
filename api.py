import requests
import json


class promptLLM:

    def __init__(self) -> None:
        self.OPENROUTER_API_KEY = "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"
    

    def prompt(self, context: str):
        return requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {self.OPENROUTER_API_KEY}",
            # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
            # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "mistralai/mixtral-8x7b-instruct", # Optional
            "messages": [
            {"role": "user", "content": context}
            ]
        })
        ).json()