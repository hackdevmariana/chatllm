import click
from rich.console import Console
from rich.prompt import Prompt, Confirm

from .common import (
    run_ollama,
    append_message,
    load_history,
)

console = Console()

MODEL = "qwen2.5-coder:7b"
MODE = "dev"


@click.command()
@click.argument("prompt", required=False)
@click.option("--history", is_flag=True, help="Usar historial persistente")
@click.option("--clear-history", is_flag=True)
def dev(prompt, history, clear_history_flag):
    MODE = "dev"
    MODEL = "qwen2.5-coder:7b"

    if clear_history_flag:
        clear_history(MODE)
        console.print("[green]Historial borrado[/green]")
        return

    messages = []

    if history:
        messages = load_history(MODE)

    if prompt:
        messages.append({"role": "user", "content": prompt})

    response = run_ollama(MODEL, messages)
    console.print(response)

    if history:
        append_message(MODE, "user", prompt)
        append_message(MODE, "assistant", response)

