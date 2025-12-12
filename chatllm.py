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
| (__| | | | (_| | |_| | | | | | | | | (_| |  __/ | | |  __/ | | (_| | |
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
def run_ollama(model, prompt=None, raw=False):
    """
    Lanza ollama interactivo, o con un prompt inicial.
    Si raw=True, imprime solo el texto devuelto.
    """
    try:
        if prompt:
            if raw:
                # Ejecuta y captura la salida para devolver solo texto
                result = subprocess.run(
                    ["ollama", "run", model],
                    input=prompt.encode(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                output = result.stdout.decode()
                console.print(output)
            else:
                subprocess.run(["ollama", "run", model], input=prompt.encode())
        else:
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
@click.option("--model", type=click.Choice(["dev", "chat"]), help="Selecciona el modelo a usar")
@click.option("--raw", is_flag=True, help="Devuelve solo el código o texto, sin banners")
@click.argument("prompt", required=False)
@click.pass_context
def cli(ctx, model, raw, prompt):
    """
    Entrada principal. Si se pasa un prompt directo y un modelo, entra en modo rápido.
    """
    console.print(f"[bold blue]{LOGO_MINIMAL}[/bold blue]")

    if model and prompt:
        if model == "dev":
            ctx.invoke(dev, prompt=prompt, raw=raw)
        else:
            ctx.invoke(chat, prompt=prompt, raw=raw)
        return

    if ctx.invoked_subcommand is None:
        print_menu()
        choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3"])
        if choice == "1":
            ctx.invoke(dev, raw=raw)
        elif choice == "2":
            ctx.invoke(chat, raw=raw)
        else:
            console.print("[yellow]Saliendo...[/yellow]")
            sys.exit(0)

# ===========================
#  SUBCOMANDOS
# ===========================
@click.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Devuelve solo el código o texto, sin banners")
def dev(prompt, raw):
    """Modo desarrollo (Qwen Coder)."""
    m = MODELS["dev"]
    if not raw:
        console.print(f"[bold {m['color']}] {BANNERS['dev']} [/bold {m['color']}]")
    run_ollama(m["model"], prompt=prompt, raw=raw)

@click.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Devuelve solo el código o texto, sin banners")
def chat(prompt, raw):
    """Modo chat general (Llama 3)."""
    m = MODELS["chat"]
    if not raw:
        console.print(f"[bold {m['color']}] {BANNERS['chat']} [/bold {m['color']}]")
    run_ollama(m["model"], prompt=prompt, raw=raw)

# ===========================
#  REGISTRAR SUBCOMANDOS
# ===========================
cli.add_command(dev)
cli.add_command(chat)

if __name__ == "__main__":
    cli()

