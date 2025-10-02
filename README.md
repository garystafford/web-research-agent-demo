# Build a Web Research Agent with Strands Agents, Ollama, Qwen3, and the Tavily MCP Server

The post [Build a Web Research Agent with Strands Agents, Ollama, Qwen3, and the Tavily MCP Server](https://garystafford.medium.com/build-a-web-research-agent-with-strands-agents-ollama-qwen3-and-the-tavily-mcp-server-8e1a1baf0f0d) guides you through building a web-based research agent using Amazon Web Services' Strands Agents, Ollama running Alibaba Cloud's Qwen3, and the Tavily MCP Server. The agent combines local, small models with cloud-powered web search, enabling it to provide up-to-date, high-quality online information. The agent is free to get started, offering 1,000 monthly API calls with Tavily.

## System Architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'edgeLabelBackground': '#ffffff', 'primaryColor': '#e7effe' }}}%%
flowchart TD
    User[User] -->|Query| Terminal[Terminal Interface]
    Terminal -->|Input| Agent[Strands Agent]
    Agent -->|Prompt| Ollama[Ollama]
    Ollama -->|Loads| Qwen3[Qwen3 Model]
    Agent -->|Tool Call| MCPClient[MCP Client]
    MCPClient -->|API Request| TavilyMCP[Tavily MCP Server]
    TavilyMCP -->|API Request| TavilyAPI[Tavily API]
    TavilyAPI -->|Web Search| Internet((Internet))
    Internet -->|Search Results| TavilyAPI
    TavilyAPI -->|Search Results| TavilyMCP
    TavilyMCP -->|Search Results| MCPClient
    MCPClient -->|Tool Response| Agent
    Qwen3 -->|Response| Ollama
    Ollama -->|Response| Agent
    Agent -->|Final Answer| Terminal
    Terminal -->|Output| User

    linkStyle default stroke:#333,stroke-width:1px,font-size:12px
```

## Featured Technologies

- **Model Context Protocol (MCP)** is an open standard that enables AI systems to interact with diverse data sources and tools, allowing for secure, two-way connections.
- **Strands Agents** is an open-source SDK developed by AWS for building AI agents using a model-driven approach. It enables developers to create intelligent agents with just a few lines of code by combining large language models (LLMs) and tool integrations.
- **Ollama** is an open-source tool that lets you run LLMs directly on your local machine, with no need for internet or cloud access. Designed for privacy and developer control, Ollama makes it easy to download, run, and manage open-source models via a simple command-line interface.
- **Qwen3** is Alibaba Cloud's latest open-source large language model series. It features both dense and Mixture-of-Experts (MoE) architectures. It introduces a unique hybrid reasoning system that allows users to switch between "thinking mode" (for in-depth, step-by-step reasoning) and "non-thinking mode" (for quick, general responses). Ollama offers Qwen3 models from 0.6 to 235 billion parameters!
- **Tavily** is a web search engine and API designed for AI agents and LLMs. It delivers fast, real-time, and accurate web information optimized for Retrieval Augmented Generation (RAG) workflows. Tavily automates searching, scraping, filtering, and content extraction via a single API call, making it easy to enrich AI apps with up-to-date, high-quality online content.
- **Tavily MCP Server** allows you to use the Tavily API from your MCP clients. It provides a suite of tools, including search, extract, map, and crawl, offering real-time web search, intelligent data extraction from web pages, powerful web mapping (creating a structured map of websites), and a web crawler that systematically explores sites.

## Getting Started on Mac

### Ollama Models

This project assumes you already have Ollama installed.

```bash
ollama pull qwen3:14b # and/or other sizes
```

### GitHub Repository

Clone this project's GitHub repository.

```bash
git clone https://github.com/garystafford/web-research-agent-demo.git

cd web-research-agent-demo/
```

### Tavily API Key

Create a free Tavily account to get your API key: [https://www.tavily.com/](https://www.tavily.com/). Update the `.env` file with your API key.

```bash
mv env.txt .env # update values
```

### Configure Python Environment and Run Agent

I have converted the project from `pip` to `uv` and `make`.

```bash
brew install uv
brew install make

make source
source .venv/bin/activate
make install

# optional: upgrade packages
make upgrade

make run
```

---

_The contents of this repository represent my viewpoints and not those of my past or current employers, including Amazon Web Services (AWS). All third-party libraries, modules, plugins, and SDKs are the property of their respective owners._
