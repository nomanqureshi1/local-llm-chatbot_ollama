# local-llm-chatbot_ollama



# Ollama Chatbot

A CLI chatbot that runs LLMs locally using Ollama with streaming responses and conversation history.

## Requirements
- Python 3.9+
- Docker
- Ollama running in Docker

## Setup
```bash
# Start Ollama container
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Pull models
docker exec ollama ollama pull llama3.1:8b

# Install dependencies
pip install requests
```

## Usage
```bash
python chatbot.py
```

## Commands

| Command | Description |
|---------|-------------|
| `/model <name>` | Switch model |
| `/temp <0-2>` | Change temperature |
| `/system <prompt>` | Change system prompt |
| `/save [filename]` | Save conversation |
| `/clear` | Clear history |
| `/help` | Show commands |
| `/quit` | Exit |

## Example
```
You: What is RAG?
AI: RAG stands for Retrieval Augmented Generation...

You: /temp 0.0
Temperature: 0.0

You: /save my_conversation
Saved to conversations/my_conversation
```
