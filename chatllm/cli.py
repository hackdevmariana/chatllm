import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box

from .chat import chat
from .dev import dev

console = Console()

LOGO_MINIMAL = r"""
       .__            __  .__  .__           
  ____ |  |__ _____ _/  |_|  | |  |   _____  
_/ ___\|  |  \\__  \\   __\  | |  |  /     \ 
\  \___|   Y  \/ __ \|  | |  |_|  |_|  Y Y  \
 \___  >___|  (____  /__| |____/____/__|_|  /
     \/     \/                     \/ 
"""

def print_menu():
    table = Table(
        title="chatllm — menú principal",
        box=box.ROUNDED,
        header_style="bold magenta",
    )
    table.add_column("Opción", style="bold cyan")
    table.add_column("Descripción")

    table.add_row("1", "Desarrollo (Qwen Coder)")
    table.add_row("2", "Chat general (Llama 3)")
    table.add_row("3", "Salir")

    console.print(table)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    console.print(f"[bold blue]{LOGO_MINIMAL}[/bold blue]")

    if ctx.invoked_subcommand is not None:
        return

    print_menu()
    choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3"])

    if choice == "1":
        ctx.invoke(dev)
    elif choice == "2":
        ctx.invoke(chat)
    else:
        console.print("[yellow]Saliendo...[/yellow]")

cli.add_command(dev)
cli.add_command(chat)

