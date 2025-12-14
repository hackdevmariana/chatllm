import click
from rich.console import Console
from rich.prompt import Prompt

from .common import (
    run_ollama,
    append_message,
    load_history,
    clear_history,
    list_sessions,
)

console = Console()

MODEL = "llama3:latest"
MODE = "chat"


@click.command()
def chat():
    session = "default"
    console.print(f"[bold green]Chat mode — session: {session}[/bold green]\n")

    while True:
        user_input = Prompt.ask(">>>")

        # -------- comandos internos --------
        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0]

            if cmd == "/exit":
                break

            elif cmd == "/history":
                history = load_history(MODE, session)
                for m in history:
                    console.print(f"[bold]{m['role']}:[/bold] {m['content']}")
                continue

            elif cmd == "/clear":
                clear_history(MODE, session)
                console.print("[yellow]History cleared[/yellow]")
                continue

            elif cmd == "/sessions":
                sessions = list_sessions(MODE)
                console.print("Sessions:", ", ".join(sessions))
                continue

            elif cmd == "/new" and len(parts) > 1:
                session = parts[1]
                console.print(f"[green]New session: {session}[/green]")
                continue

            elif cmd == "/switch" and len(parts) > 1:
                session = parts[1]
                console.print(f"[green]Switched to session: {session}[/green]")
                continue

            else:
                console.print("[red]Unknown command[/red]")
                continue

        # -------- mensaje normal --------
        append_message(MODE, session, "user", user_input)
        history = load_history(MODE, session)

        response = run_ollama(MODEL, history)

        append_message(MODE, session, "assistant", response)
        console.print(response)

