#!/usr/bin/env python3
import click
import subprocess
import sys
import shlex
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box

console = Console()

# ===========================
#  BANNERS ASCII
# ===========================

BANNERS = {
    "dev": """
╔══════════════════════════════════════╗
║     🚀  QWEN CODER - DEV MODE        ║
╚══════════════════════════════════════╝
""",
    "chat": """
╔══════════════════════════════════════╗
║     💬   LLAMA 3 - GENERAL CHAT      ║
╚══════════════════════════════════════╝
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
    Lanza ollama interactivo, o con un prompt inicial.
    """
    try:
        if prompt:
            # Ejecuta ollama run con texto directo (modo no interactivo)
            subprocess.run(["ollama", "run", model], input=prompt.encode())
        else:
            # Modo interactivo normal
            subprocess.run(["ollama", "run", model])
    except FileNotFoundError:
        console.print("[red]Error: ollama no está instalado o no está en el PATH.[/red]")
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
@click.argument("prompt", required=False)
@click.pass_context
def cli(ctx, prompt):
    """
    Entrada principal. Si se pasa un prompt directo, entra en modo rápido.
    """
    if prompt:
        console.print(f"[bold green]Prompt directo detectado:[/bold green] {prompt}")
        ctx.invoke(chat, prompt=prompt)
        return

    if ctx.invoked_subcommand is None:
        console.print("\n[bold magenta]=== chatllm ===[/bold magenta]\n")
        print_menu()

        choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3"])

        if choice == "1":
            ctx.invoke(dev)
        elif choice == "2":
            ctx.invoke(chat)
        else:
            console.print("[yellow]Saliendo...[/yellow]")
            sys.exit(0)


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

