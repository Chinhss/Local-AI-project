import httpx
from local_ai.ollama_client import OllamaClient
from local_ai.storage import load_history, save_history

HELP_TEXT = """Available commands:
  /clear    clear the conversation history
  /history  show the conversation so far
  /model    show the current model
  /help     show this message
  /exit     quit Son"""

def show_history(client: OllamaClient) -> None:
    if not client.messages:
        print("[No messages yet.]")
        return

    for message in client.messages:
        speaker = "You" if message["role"] == "user" else "Son"
        print(f"{speaker} > {message['content']}\n")

def handle_command(command: str, client: OllamaClient) -> bool:
    """Run a slash command. Returns False if Son should quit."""
    name = command.strip().lower()

    if name in ("/exit", "/quit"):
        return False
    elif name == "/clear":
        client.clear()
        save_history(client.messages)
        print("[Conversation cleared.]")
    elif name == "/history":
        show_history(client)
    elif name == "/model":
        print(f"Current model: {client.model}")
    elif name == "/help":
        print(HELP_TEXT)
    else:
        print(f"Unknown command: {command}. Type /help for a list of commands.")
    
    print()
    return True

def main():
    client = OllamaClient()
    client.messages = load_history()

    print("Son - Local AI")
    print(f"Model: {client.model}")
    print("Type 'exit' to quit.")
    print()

    while True:
        try:
            prompt = input("You > ")
        except (KeyboardInterrupt, EOFError):
            print("")
            break

        if prompt.lower() == "exit":
            break

        if not prompt.strip():
            continue

        if prompt.startswith("/"):
            if not handle_command(prompt, client):
                break
            continue
        
        print("Son > ", end="", flush=True)

        try:
            for chunk in client.stream_chat(prompt):
                print(chunk, end="", flush=True)
            save_history(client.messages)
        except httpx.ConnectError:
            print(f"\n[Could not reach Ollama at {client.base_url}. Is it running?]")
        except KeyboardInterrupt:
            print("\n[Interrupted]")

        print()
        print()

if __name__ == "__main__":
    main()