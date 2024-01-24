import json

import requests

FASTGPT_API = "fastgpt-JgHWU7xd6DHsLxQ3badljRB3eSFMm"
BASE_URL = "https://api.fastgpt.in/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {FASTGPT_API}",
    "Content-Type": "application/json"
}
payload = {
    "stream": False,
    "detail": False,
    "variables": {
        "uid": "",
        "name": ""
    },
    "messages": [
        {
            "content": "歼-16战机有几个发动机",
            "role": "user"
        }
    ]
}
response = requests.post(BASE_URL, json=payload, headers=headers)
print(json.loads(response.text)["choices"][0]["message"]["content"])
