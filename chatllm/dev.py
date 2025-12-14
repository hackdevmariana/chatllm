import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from pathlib import Path

from .common import run_ollama, load_history, save_history, append_message, clear_history

console = Console()

SESSION = "default"

@click.command()
@click.argument("prompt", required=False)
def dev(prompt):
    global SESSION

    console.print(f"[bold cyan]Dev mode — session: {SESSION}[/bold cyan]")

    while True:
        if not prompt:
            user_input = Prompt.ask(">>>")
        else:
            user_input = prompt
            prompt = None  # Solo usar prompt inicial si lo hay

        user_input = user_input.strip()

        # Comandos internos
        if user_input.startswith("/"):
            if user_input == "/history":
                history = load_history(f"dev_{SESSION}")
                if not history:
                    console.print("[yellow]No hay historial.[/yellow]")
                else:
                    for msg in history:
                        console.print(f"{msg['role']}: {msg['content']}")
                continue

            if user_input.startswith("/new "):
                SESSION = user_input.split(maxsplit=1)[1]
                console.print(f"[green]Nueva sesión: {SESSION}[/green]")
                continue

            if user_input.startswith("/switch "):
                SESSION = user_input.split(maxsplit=1)[1]
                console.print(f"[green]Cambiada a sesión: {SESSION}[/green]")
                continue

            if user_input == "/clear":
                clear_history(f"dev_{SESSION}")
                console.print("[green]Historial borrado.[/green]")
                continue

            if user_input == "/sessions":
                # Listar todas las sesiones en dev
                from pathlib import Path
                files = list(Path.home().joinpath(".local/share/chatllm").glob("dev_*_history.json"))
                sessions = [f.stem.replace("dev_", "").replace("_history","") for f in files]
                console.print("Sessions:", ", ".join(sessions) if sessions else "Ninguna")
                continue

            if user_input.startswith("/save "):
                filename = user_input.split(maxsplit=1)[1]
                history = load_history(f"dev_{SESSION}")
                with open(filename, "w") as f:
                    for msg in history:
                        f.write(f"{msg['role']}: {msg['content']}\n")
                console.print(f"[green]Historial guardado en {filename}[/green]")
                continue

        # Guardar el mensaje del usuario
        append_message(f"dev_{SESSION}", "user", user_input)

        # Llamada a Ollama
        messages = load_history(f"dev_{SESSION}")
        response = run_ollama("qwen2.5-coder:7b", messages)

        append_message(f"dev_{SESSION}", "assistant", response)
        console.print(f"[bold green]{response}[/bold green]")

