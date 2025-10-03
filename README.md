# Build a Web Research Agent with Strands Agents, Ollama, Qwen3, and the Tavily MCP Server

The post [Build a Web Research Agent with Strands Agents, Ollama, Qwen3, and the Tavily MCP Server](https://garystafford.medium.com/build-a-web-research-agent-with-strands-agents-ollama-qwen3-and-the-tavily-mcp-server-8e1a1baf0f0d) guides you through building a web-based research agent using Amazon Web Services' Strands Agents, Ollama running Alibaba Cloud's Qwen3, and the Tavily MCP Server. The agent combines local, small models with cloud-powered web search, enabling it to provide up-to-date, high-quality online information. The agent is free to get started, offering 1,000 monthly API calls with Tavily.

## System Architecture

```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#e7effe',
      'primaryTextColor': '#333',
      'primaryBorderColor': '#333',
      'lineColor': '#333',
      'secondaryColor': '#fff',
      'tertiaryColor': '#fff',
      'fontFamily': 'arial',
      'background': '#fff'
    }
  }
}%%

flowchart TD
    %% Force background color using HTML-like styling
    classDef bg fill:#ffffff

    %% Create invisible background node covering the whole area
    bg[" "]:::bg
    style bg fill:#ffffff,stroke:none,color:#ffffff

    %% Local Resources (use specific coloring)
    classDef localResource fill:#e7effe,stroke:#333,stroke-width:1px
    User[User]:::localResource
    Terminal[Terminal Interface]:::localResource
    Agent[Strands Agent]:::localResource
    Ollama[Ollama]:::localResource
    Qwen3[Qwen3 Model]:::localResource
    MCPClient[MCP Client]:::localResource

    %% Remote Resources (use specific coloring)
    classDef remoteResource fill:#f9d0c4,stroke:#333,stroke-width:1px
    TavilyMCP[Tavily MCP Server]:::remoteResource
    TavilyAPI[Tavily API]:::remoteResource
    Internet((Internet)):::remoteResource

    %% Flow connections
    User -->|Query| Terminal
    Terminal -->|Input| Agent
    Agent -->|Prompt| Ollama
    Ollama -->|Loads| Qwen3
    Agent -->|Tool Call| MCPClient
    MCPClient -->|API Request| TavilyMCP
    TavilyMCP -->|API Request| TavilyAPI
    TavilyAPI -->|Web Search| Internet
    Internet -->|Search Results| TavilyAPI
    TavilyAPI -->|Search Results| TavilyMCP
    TavilyMCP -->|Search Results| MCPClient
    MCPClient -->|Tool Response| Agent
    Qwen3 -->|Response| Ollama
    Ollama -->|Response| Agent
    Agent -->|Final Answer| Terminal
    Terminal -->|Output| User

    %% Style for all connections
    linkStyle default stroke:#333,stroke-width:1px,font-size:12px

    %% Legend at the bottom of the diagram
    subgraph Legend
        LocalRes[Local Resources]:::localResource
        RemoteRes[Remote Resources]:::remoteResource
    end
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

### Configure Python Environment

The project has been converted from `pip` to `uv` and `make`. Install `uv` and `make`.

```bash
brew install uv
brew install make

uv --version
make --version
```

Create and activate a Python virtual environment, then install the required packages.

```bash
make source
source .venv/bin/activate

make install
uv tree --depth 1
```

Optionally, upgrade the packages.

```bash
make upgrade
```

### Run the Agent

```bash
make run
```

### Example Prompts

Try these example prompts:

- "What are the latest advancements in renewable energy technologies?"
- "Summarize the key points from a recent articles about AI ethics."
- "Find recent news about space exploration missions."
- "What are the current trends in remote work and its impact on productivity?"
- "Provide a summary of recent developments in electric vehicle technology."
- "What is some of the latest technology news out of NVIDIA?"
- "What are the recent breakthroughs in cancer research?"
- "Summarize the main points from this scientific paper: https://arxiv.org/html/1706.03762v7"

### Troubleshooting

If you encounter issues, consider the following:

- Ensure Ollama is running and the specified model is downloaded.
- Verify your Tavily API key is correct and has not exceeded the free tier limit.
- Check your internet connection for accessing the Tavily API.
- Review the `.env` file for correct environment variable settings.
- Look for error messages in the terminal output to identify specific problems.
- Consult the documentation for Strands Agents, Ollama, and Tavily for additional help.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

_The contents of this repository represent my viewpoints and not those of my past or current employers, including Amazon Web Services (AWS). All third-party libraries, modules, plugins, and SDKs are the property of their respective owners._
