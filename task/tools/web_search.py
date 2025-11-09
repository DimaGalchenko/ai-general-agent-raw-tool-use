from typing import Any

import requests

from task.tools.base import BaseTool


class WebSearchTool(BaseTool):

    def __init__(self, open_ai_api_key: str):
        self.__api_key = f"Bearer {open_ai_api_key}"
        self.__endpoint = "https://api.openai.com/v1/chat/completions"

    # Sample of tool config:
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "web_search_tool",
    #         "description": "Tool for WEB searching.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "request": {
    #                     "type": "string",
    #                     "description": "The search query or question to search for on the web"
    #                 }
    #             },
    #             "required": [
    #                 "request"
    #             ]
    #         }
    #     }
    # }

    @property
    def name(self) -> str:
        # TODO: Provide tool name as `web_search_tool`
        return 'web_search_tool'

    @property
    def description(self) -> str:
        # TODO: Provide description of this tool
        return "Tool that provides ability to search in the WEB."

    @property
    def input_schema(self) -> dict[str, Any]:
        # TODO: Provide tool params Schema (it applies `request` string to search by)
        return {
            "type": "object",
            "properties": {
                "request": {
                    "type": "string",
                    "description": "The search query or question to search for on the web."
                }
            },
            "required": ["request"]
        }

    def execute(self, arguments: dict[str, Any]) -> str:
        headers = {
            "Authorization": self.__api_key,
            "Content-Type": "application/json"
        }

        request_data = {
            "model": "gpt-4o-mini-search-preview",  # or "gpt-4o-search-preview"
            "messages": [
                {"role": "user", "content": str(arguments["request"])}
            ]
        }

        response = requests.post(
            url=self.__endpoint,
            headers=headers,
            json=request_data
        )

        if response.status_code == 200:
            try:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                return f"Error parsing response: {e}"
        else:
            raise Exception(f"Error: {response.status_code} {response.text}")
