from typing import Any

import requests

from task.tools.base import BaseTool


class WebSearchTool(BaseTool):

    def __init__(self, open_ai_api_key: str):
        self.__api_key = f"Bearer {open_ai_api_key}"
        self.__endpoint = "https://api.openai.com/v1/chat/completions"

    @property
    def name(self) -> str:
        return 'web_search_tool'

    @property
    def description(self) -> str:
        return 'Makes Search in WEB by request'

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "web_search_tool",
                "description": "Tool for WEB searching.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "request": {
                            "type": "string",
                            "description": "The search query or question to search for on the web"
                        }
                    },
                    "required": [
                        "request"
                    ]
                }
            }
        }

    def execute(self, arguments: dict[str, Any]) -> str:
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json"
        }
        request_data = {
            "model": "gpt-4o-search-preview",
            "messages": [{"role": "user", "content": str(arguments["request"])}],
            "tools": [{"type": "static_function",
                       "static_function": {"name": "google_search", "description": "Grounding with Google Search",
                                           "configuration": {}}}],
            "temperature": 0
        }
        response = requests.post(self.__endpoint, headers=headers, json=request_data)
        if response.status_code == 200:
            return response.json()[0]["message"]["content"]
        return f"Error: {response.json()['error']}"
