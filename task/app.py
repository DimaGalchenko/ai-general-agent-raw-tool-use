import os

from task.constants import OPENAI_API_KEY
from task.openai_client import OpenAIClient
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role
from task.prompts import SYSTEM_PROMPT
from task.tools.users.create_user_tool import CreateUserTool
from task.tools.users.delete_user_tool import DeleteUserTool
from task.tools.users.get_user_by_id_tool import GetUserByIdTool
from task.tools.users.search_users_tool import SearchUsersTool
from task.tools.users.update_user_tool import UpdateUserTool
from task.tools.users.user_client import UserClient
from task.tools.web_search import WebSearchTool

def main():
    #TODO:
    # 1. Create UserClient
    # 2. Create OpenAIClient with all tools (WebSearchTool, GetUserByIdTool, SearchUsersTool, CreateUserTool, UpdateUserTool, DeleteUserTool)
    # 3. Create Conversation and add there first System message with SYSTEM_PROMPT (you need to write it in task.prompts#SYSTEM_PROMPT)
    # 4. Run infinite loop and in loop and:
    #    - get user input from terminal (`input("> ").strip()`)
    #    - Add User message to Conversation
    #    - Call OpenAIClient with conversation history
    #    - Add Assistant message to Conversation and print its content
    user_client = UserClient()
    openai_client = OpenAIClient(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY,
        tools=[
            WebSearchTool(OPENAI_API_KEY),
            GetUserByIdTool(user_client),
            SearchUsersTool(user_client),
            CreateUserTool(user_client),
            UpdateUserTool(user_client),
            DeleteUserTool(user_client),
        ]
    )
    messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]
    while True:
        user_reqeust = input("> ").strip()
        messages.append(Message(role=Role.USER, content=user_reqeust))
        response = openai_client.get_completion(messages=messages)
        messages.append(response)
        print(f'AI response: {response.content}')


main()

#TODO:
# Implement it with Anthropic orchestration model
# https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview#single-tool-example