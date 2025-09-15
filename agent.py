# This script sets up an interactive terminal-based agent that uses the Tavily MCP server to search the internet and answer user queries.
# Author: Gary Stafford
# Date: 2025-09-13
# References:
# https://github.com/tavily-ai/tavily-mcp
# https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/#2-streamable-http

import logging
import os
import sys

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models.ollama import OllamaModel
from strands.tools.mcp.mcp_client import MCPClient
from strands_tools import current_time, shell

# Set up basic logging configuration
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
MODEL_ID = os.getenv("MODEL_ID", "qwen3:4b")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# Initialize the model
model = OllamaModel(
    model_id=MODEL_ID,
    temperature=TEMPERATURE,
    host="http://localhost:11434",
    keep_alive="10m",
)

logger.info(f"Model configuration: {model.config}")

# Create a conversation manager
conversation_manager = SlidingWindowConversationManager(
    window_size=20,
)

# Define a system prompt for the agent
system_prompt = """You are a helpful assistant that can search the internet to provide information and answer questions based on the latest news and data. 
You can also determine the current date and time, and execute shell commands on the local machine, if necessary."""

# Initialize the MCP client for Tavily with your API key
streamable_http_mcp_client = MCPClient(
    lambda: streamablehttp_client(
        f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
    )
)

with streamable_http_mcp_client:
    # Create an agent with these tools
    tools = [current_time, shell, streamable_http_mcp_client.list_tools_sync()]

    agent = Agent(
        system_prompt=system_prompt,
        model=model,
        tools=tools,
        conversation_manager=conversation_manager,
    )

    # Interactive terminal loop
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print(f"{BLUE}Welcome to the Tavily MCP Server Search Agent!{RESET}")
    while True:
        try:
            user_input = input(f"\n{BLUE}> {RESET}")

            if user_input.lower() == "exit" or user_input.lower() == "quit":
                print(f"\n{BLUE}Goodbye! 👋{RESET}")
                break

            response = agent(user_input)
            print(
                f"\n{GREEN}{response.message['content'][0]['text'].split('</think>\n\n')[-1]}{RESET}"
            )
            logger.info(f"Agent metrics: {response.metrics}")
        except KeyboardInterrupt:
            print(f"\n\n{RED}Execution interrupted. Exiting...{RESET}")
            break
        except Exception as e:
            print(f"\n{RED}An error occurred: {str(e)}{RESET}")
            print(f"{RED}Please try a different request.{RESET}")
