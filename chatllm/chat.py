import click
from rich.console import Console
from rich.prompt import Prompt

from .common import (
    load_history,
    append_message,
    clear_history,
    run_ollama,
)

console = Console()

MODEL = "llama3:latest"
MODE = "chat"

@click.command()
@click.option("--clear", is_flag=True, help="Borrar historial")
def chat(clear):
    if clear:
        clear_history(MODE)
        console.print("[green]Historial borrado[/green]")
        return

    console.print("[bold green]Chat general (historial persistente)[/bold green]")
    history = load_history(MODE)

    while True:
        try:
            user_input = Prompt.ask(">>>")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Saliendo[/yellow]")
            break

        append_message(MODE, "user", user_input)
        history = load_history(MODE)

        response = run_ollama(MODEL, history)
        console.print(response)

        append_message(MODE, "assistant", response)

