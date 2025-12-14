import click
from rich.prompt import Prompt
from .common import MODELS, BANNERS, run_ollama, console


@click.command()
def chat():
    """Interactive general chat (ChatGPT-style)."""
    m = MODELS["chat"]

    console.print(f"[bold {m['color']}]{BANNERS['chat']}[/bold {m['color']}]")
    console.print("[dim]Type /exit or Ctrl+C to leave[/dim]\n")

    try:
        while True:
            user_input = Prompt.ask("[bold cyan]>>>[/bold cyan]")
            if user_input.strip().lower() in {"/exit", "/quit"}:
                console.print("[yellow]Leaving chat...[/yellow]")
                break

            response = run_ollama(m["model"], user_input)
            console.print(f"\n[bold green]<<<[/bold green] {response}\n")

    except KeyboardInterrupt:
        console.print("\n[yellow]Chat interrupted[/yellow]")

