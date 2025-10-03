FROM ghcr.io/astral-sh/uv:0.8.19-python3.13-bookworm-slim

# Create a non-root user named 'appuser'
RUN useradd -m appuser

# Set the working directory for the user
WORKDIR /home/appuser

# Configure UV for container environment
ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1

# Copy project files
COPY . .

RUN uv venv
RUN uv sync --no-dev --no-cache

# Set environment variables - can be overridden with docker run -e
ENV MODEL_ID="qwen3:30b" \
    TEMPERATURE="0.2" \
    BYPASS_TOOL_CONSENT="True" \
    OLLAMA_HOST="http://host.docker.internal:11434" \
    KEEP_ALIVE="10m" \
    LOG_LEVEL="WARNING"

# Switch to the 'appuser' for subsequent instructions and container runtime
USER appuser

# Run the agent
CMD ["uv", "run", "agent.py"]