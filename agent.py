# This script sets up an interactive terminal-based agent that uses the Tavily MCP server to search the internet and answer user queries.
# Author: Gary Stafford
# Date: 2025-10-02
# References:
# https://github.com/tavily-ai/tavily-mcp
# https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/#2-streamable-http

import logging
import os
import readline  # Add readline for proper terminal input handling
import signal
import sys
from typing import Any, Dict, Union

from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.models.ollama import OllamaModel
from strands.tools.mcp.mcp_client import MCPClient
from strands_tools import current_time, shell


# Terminal colors
class TermColors:
    """ANSI color codes for terminal output styling."""

    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"


# Set up basic logging configuration
def setup_logging(log_level: str = "WARNING") -> logging.Logger:
    """Configure logging with the specified log level.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Logger instance
    """
    level = getattr(logging, log_level.upper(), logging.WARNING)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        stream=sys.stdout,
    )
    return logging.getLogger(__name__)


# Load environment variables with validation
def load_environment_variables() -> Dict[str, Any]:
    """Load and validate required environment variables.

    Returns:
        Dictionary containing environment variables

    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    env_vars = {
        "MODEL_ID": os.getenv("MODEL_ID", "qwen3:14b"),
        "TEMPERATURE": float(os.getenv("TEMPERATURE", 0.2)),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
        "OLLAMA_HOST": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "KEEP_ALIVE": os.getenv("KEEP_ALIVE", "10m"),
    }

    # Validate required environment variables
    if not env_vars["TAVILY_API_KEY"]:
        raise ValueError("TAVILY_API_KEY environment variable is required")

    return env_vars


# Initialize the model
def initialize_model(
    model_id: str, temperature: float, host: str, keep_alive: str
) -> OllamaModel:
    """Initialize the Ollama model with the specified parameters.

    Args:
        model_id: ID of the model to use
        temperature: Temperature parameter for generation
        host: Ollama host URL
        keep_alive: Keep-alive duration

    Returns:
        Configured OllamaModel instance
    """
    return OllamaModel(
        model_id=model_id,
        temperature=temperature,
        host=host,
        keep_alive=keep_alive,
    )


# Initialize the MCP client for Tavily
def initialize_mcp_client(api_key: str) -> MCPClient:
    """Initialize the MCP client for Tavily.

    Args:
        api_key: Tavily API key

    Returns:
        Configured MCPClient instance
    """
    return MCPClient(
        lambda: streamablehttp_client(
            f"https://mcp.tavily.com/mcp/?tavilyApiKey={api_key}"
        )
    )


# Process user input
def process_input(user_input: str) -> Union[bool, str]:
    """Process user input and check for exit commands.

    Args:
        user_input: User's input string

    Returns:
        False if user wants to exit, otherwise the processed input
    """
    # Strip whitespace
    cleaned_input = user_input.strip()

    # Check for exit commands
    if cleaned_input.lower() in ["exit", "quit", "q", "bye"]:
        return False

    # Return processed input
    return cleaned_input


# Format agent response
def format_response(response: Any, logger: logging.Logger) -> str:
    """Format the agent's response for display.

    Args:
        response: Response from the agent
        logger: Logger instance for logging

    Returns:
        Formatted response string
    """
    try:
        # Extract the actual response text, removing any thinking content
        response_text = response.message["content"][0]["text"]
        # Remove the thinking part if it exists (content after </think>)
        if "</think>" in response_text:
            return response_text.split("</think>\n\n")[-1]
        return response_text
    except (KeyError, IndexError) as e:
        logger.warning(f"Error formatting response: {e}")
        return "Sorry, I couldn't process that response correctly."


# Graceful shutdown handler
def setup_signal_handlers() -> None:
    """Set up signal handlers for graceful shutdown."""

    def signal_handler(sig, frame):
        print(
            f"\n\n{TermColors.YELLOW}Received signal {sig}. Shutting down gracefully...{TermColors.RESET}"
        )
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


# Main interactive loop
def run_interactive_loop(agent: Agent, logger: logging.Logger) -> None:
    """Run the main interactive loop for the agent.

    Args:
        agent: The configured Agent instance
        logger: Logger instance for logging
    """
    print(
        f"{TermColors.BLUE}Welcome to the Tavily MCP Server Search Agent!{TermColors.RESET}"
    )
    print(
        f"{TermColors.BLUE}Type 'exit' or 'quit' to end the session.{TermColors.RESET}"
    )

    while True:
        try:
            user_input = input(f"\n{TermColors.BLUE}> {TermColors.RESET}")
            processed_input = process_input(user_input)

            # Check if user wants to exit
            if processed_input is False:
                print(f"\n{TermColors.BLUE}Goodbye! 👋{TermColors.RESET}")
                break

            # Get response from agent
            response = agent(processed_input)
            formatted_response = format_response(response, logger)

            # Display response
            print(f"\n{TermColors.GREEN}{formatted_response}{TermColors.RESET}")

            # Log metrics at debug level
            logger.debug(f"Agent metrics: {response.metrics}")

        except KeyboardInterrupt:
            print(
                f"\n\n{TermColors.YELLOW}Execution interrupted. Exiting...{TermColors.RESET}"
            )
            break
        except ConnectionError as e:
            print(f"\n{TermColors.RED}Connection error: {str(e)}{TermColors.RESET}")
            print(
                f"{TermColors.RED}Check if Ollama is running and try again.{TermColors.RESET}"
            )
        except ValueError as e:
            print(f"\n{TermColors.RED}Value error: {str(e)}{TermColors.RESET}")
            print(
                f"{TermColors.RED}Please check your input and try again.{TermColors.RESET}"
            )
        except Exception as e:
            print(f"\n{TermColors.RED}An error occurred: {str(e)}{TermColors.RESET}")
            print(f"{TermColors.RED}Please try a different request.{TermColors.RESET}")
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)


# Configure readline for proper input handling
def configure_readline() -> None:
    """Configure readline for proper terminal input handling."""
    # Enable tab completion
    readline.parse_and_bind("tab: complete")

    # Set up history file
    histfile = os.path.join(os.path.expanduser("~"), ".search_agent_history")
    try:
        readline.read_history_file(histfile)
        # Default history length
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    # Save history on exit
    import atexit

    atexit.register(readline.write_history_file, histfile)


# Main function
def main() -> None:
    """Main entry point of the application."""
    # Setup signal handlers for graceful shutdown
    setup_signal_handlers()

    # Configure readline for proper input handling
    configure_readline()

    # Setup logging
    logger = setup_logging(os.getenv("LOG_LEVEL", "WARNING"))

    try:
        # Load environment variables
        env = load_environment_variables()

        # Initialize model
        model = initialize_model(
            env["MODEL_ID"], env["TEMPERATURE"], env["OLLAMA_HOST"], env["KEEP_ALIVE"]
        )

        logger.debug(f"Model configuration: {model.config}")

        # Create a conversation manager
        conversation_manager = SlidingWindowConversationManager(
            window_size=20,
        )

        # Define a system prompt for the agent
        system_prompt = """You are a helpful research assistant that can search the internet to provide information and answer questions based on the latest news and data.
        
        Important:
        1. Always check the latest date and time before providing time-sensitive information.
        2. Always respond in markdown format for better readability.
        3. If you cannot find the information, respond with "I don't know" or "I cannot find the information".
        4. If you are unsure about the information, indicate your uncertainty in your response.
        5. Use the tools at your disposal to gather information and provide accurate answers.
        6. Be concise and to the point in your responses.
        7. Cite your sources when providing information from the web.
        """

        # Initialize MCP client
        streamable_http_mcp_client = initialize_mcp_client(env["TAVILY_API_KEY"])

        with streamable_http_mcp_client:
            # Create an agent with these tools
            tools = [current_time, shell, streamable_http_mcp_client.list_tools_sync()]

            agent = Agent(
                system_prompt=system_prompt,
                model=model,
                tools=tools,
                conversation_manager=conversation_manager,
            )

            # Run the interactive loop
            run_interactive_loop(agent, logger)

    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        print(f"{TermColors.RED}Fatal error: {str(e)}{TermColors.RESET}")
        sys.exit(1)


# Entry point
if __name__ == "__main__":
    main()
