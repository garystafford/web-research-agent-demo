# linux/amd64 version for ECS: https://github.com/astral-sh/uv/pkgs/container/uv/520833613?tag=python3.13-bookworm-slim
FROM ghcr.io/astral-sh/uv:0.8.19-python3.13-bookworm-slim

# Create a non-root user named 'appuser'
RUN useradd -m appuser

# Set the working directory for the user
WORKDIR /home/appuser

# Configure UV for container environment
ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1

# Copy project files
COPY . .

RUN uv venv .venv
RUN uv sync

# Set environment variables - can be overridden with docker run -e
ENV MODEL_ID="qwen3:30b" \
    TEMPERATURE="0.2" \
    BYPASS_TOOL_CONSENT="True" \
    OLLAMA_HOST="http://host.docker.internal:11434" \
    KEEP_ALIVE="10m" \
    LOG_LEVEL="WARNING"

# Expose Ollama port (only needed if running Ollama within this container)
# EXPOSE 11434

# Switch to the 'appuser' for subsequent instructions and container runtime
USER appuser


# Run the agent
CMD ["uv", "run", "agent.py"]