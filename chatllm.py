#!/usr/bin/env python3
import click
import subprocess
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box

console = Console()

# ===========================
#  LOGO MINIMALISTA PRINCIPAL
# ===========================

LOGO_MINIMAL = r"""
       .__            __  .__  .__           
  ____ |  |__ _____ _/  |_|  | |  |   _____  
_/ ___\|  |  \\__  \\   __\  | |  |  /     \ 
\  \___|   Y  \/ __ \|  | |  |_|  |_|  Y Y  \
 \___  >___|  (____  /__| |____/____/__|_|  /
     \/     \/     \/                     \/ 
"""

# ===========================
#  BANNERS POR MODELO
# ===========================

BANNERS = {
    "dev": r"""
      _           _   _ _                 _            
     | |         | | | | |               | |           
  ___| |__   __ _| |_| | |_ __ ___     __| | _____   __
 / __| '_ \ / _` | __| | | '_ ` _ \   / _` |/ _ \ \ / /
| (__| | | | (_| | |_| | | | | | | | (_| |  __/\ V / 
 \___|_| |_|\__,_|\__|_|_|_| |_| |_|  \__,_|\___| \_/  
""",
    "chat": r"""
      _           _   _ _                                             _ 
     | |         | | | | |                                           | |
  ___| |__   __ _| |_| | |_ __ ___     __ _  ___ _ __   ___ _ __ __ _| |
 / __| '_ \ / _` | __| | | '_ ` _ \   / _` |/ _ \ '_ \ / _ \ '__/ _` | |
| (__| | | | (_| | |_| | | | | | | | (_| |  __/ | | |  __/ | | (_| | |
 \___|_| |_|\__,_|\__|_|_|_| |_| |_|  \__, |\___|_| |_|\___|_|  \__,_|_|
                                       __/ |                            
                                      |___/                             
"""
}

# ===========================
#  MODELOS DISPONIBLES
# ===========================

MODELS = {
    "dev": {
        "name": "Qwen 2.5 Coder",
        "model": "qwen2.5-coder:7b",
        "color": "cyan"
    },
    "chat": {
        "name": "Llama 3",
        "model": "llama3:latest",
        "color": "green"
    }
}

# ===========================
#  FUNCIONES
# ===========================

def run_ollama(model, prompt=None):
    """
    Lanza Ollama interactivo, o con un prompt inicial.
    """
    try:
        if prompt:
            subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode(),
                check=True
            )
        else:
            subprocess.run(["ollama", "run", model], check=True)
    except FileNotFoundError:
        console.print("[red]Error: Ollama no está instalado o no está en el PATH.[/red]")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error ejecutando Ollama: {e}[/red]")
        sys.exit(1)

def print_menu():
    table = Table(
        title="chatllm — menú principal",
        box=box.ROUNDED,
        header_style="bold magenta"
    )
    table.add_column("Opción", style="bold cyan")
    table.add_column("Descripción")

    table.add_row("1", "Desarrollo (Qwen Coder)")
    table.add_row("2", "Chat general (Llama 3)")
    table.add_row("3", "Salir")

    console.print(table)

# ===========================
#  CLI PRINCIPAL
# ===========================

@click.group(invoke_without_command=True)
@click.option("--model", type=click.Choice(["dev", "chat"]), help="Selecciona el modelo para prompt directo")
@click.argument("prompt", required=False)
@click.pass_context
def cli(ctx, model, prompt):
    """
    Entrada principal. Si se pasa un prompt directo, entra en modo rápido.
    """
    console.print(f"[bold blue]{LOGO_MINIMAL}[/bold blue]")

    if prompt:
        target = model or "chat"
        console.print(f"[bold green]Prompt directo detectado para {target}:[/bold green] {prompt}")
        ctx.invoke(chat if target=="chat" else dev, prompt=prompt)
        return

    if ctx.invoked_subcommand is None:
        print_menu()
        choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3"])

        if choice == "1":
            ctx.invoke(dev)
        elif choice == "2":
            ctx.invoke(chat)
        else:
            if Prompt.ask("¿Seguro que quieres salir?", choices=["y","n"]) == "y":
                console.print("[yellow]Saliendo...[/yellow]")
                sys.exit(0)
            else:
                cli()  # vuelve al menú

# ===========================
#  SUBCOMANDOS
# ===========================

@cli.command()
@click.argument("prompt", required=False)
def dev(prompt):
    """Modo desarrollo (Qwen Coder)."""
    m = MODELS["dev"]
    console.print(f"[bold {m['color']}] {BANNERS['dev']} [/bold {m['color']}]")
    run_ollama(m["model"], prompt=prompt)

@cli.command()
@click.argument("prompt", required=False)
def chat(prompt):
    """Modo chat general (Llama 3)."""
    m = MODELS["chat"]
    console.print(f"[bold {m['color']}] {BANNERS['chat']} [/bold {m['color']}]")
    run_ollama(m["model"], prompt=prompt)

if __name__ == "__main__":
    cli()

