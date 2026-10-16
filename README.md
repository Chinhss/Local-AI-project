# Son: a local AI assistant for the terminal

Son is a personal AI assistant I'm building in Python. It runs on my own laptop through [Ollama](https://ollama.com), so everyday use needs no cloud service and my data stays on my machine. Later it will be able to switch to a cloud model (Claude) for harder tasks, and it will gain tools for coding help, email drafts, and calendar and deadline tracking.

This is a learning project: I'm writing it step by step to understand how local inference, tool calling, permissions and agent design actually work.

## Current status

Working now:

- Interactive chat in the terminal with streaming replies
- Conversation memory within a session, saved to disk so Son remembers the last conversation (`~/.son/history.json`)
- A system prompt that gives Son its identity and a short, direct style
- Error handling: a clear message if Ollama isn't running, and Ctrl+C stops an answer or quits cleanly
- Slash commands: `/help`, `/history`, `/model`, `/clear`, `/exit`

Default model: `qwen3-coder:30b`, running through Ollama on a laptop with an 8 GB GPU and 24 GB RAM.

## Setup

Requirements: Python 3.11+, Git, and Ollama.

```powershell
# 1. Get the model
ollama pull qwen3-coder:30b

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install Son in editable mode (this creates the `son` command)
pip install -e .

# 4. Run it
son
```

On Linux or macOS, activate with `source .venv/bin/activate` instead.

## Commands

| Command    | What it does                            |
| ---------- | --------------------------------------- |
| `/help`    | List the available commands             |
| `/history` | Show the conversation so far            |
| `/model`   | Show the current model                  |
| `/clear`   | Clear the conversation (and saved copy) |
| `/exit`    | Quit Son                                |

## Project layout

```
src/local_ai/
  cli.py            interactive loop and slash commands
  ollama_client.py  talks to the Ollama API (chat, streaming, history)
  prompts.py        the system prompt
  storage.py        saving and loading conversation history
```

## Roadmap

Next:

1. A first read-only tool, so Son can list and read files on request
2. A permission layer in front of every tool, so the model asks my code for access instead of acting on its own
3. Settings in one place (model, Ollama URL), then switching between models

Later:

- A model router: local by default, optional Claude through the Anthropic API for difficult tasks
- Coding help: Git and repository awareness
- Email: read and classify, and write drafts for me to review, never auto-sending important messages
- Calendar: add and update deadlines
- DCU Loop: collect deadlines with plain code, with the model only interpreting ambiguous details
- SQLite for local state, and scheduled background checks instead of an always-running model
- Moving the whole setup from Windows to Linux

## Design principles

- **Local first.** Cloud models are opt-in, not the default.
- **The model never holds credentials.** Tools hold the access and my code decides what's allowed.
- **Drafts, not sends.** Anything important waits for my approval.