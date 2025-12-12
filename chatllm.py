#!/usr/bin/env python3
import click
import subprocess
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
import re

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
     \/     \/                     \/ 
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
    "dev": {"name": "Qwen 2.5 Coder", "model": "qwen2.5-coder:7b", "color": "cyan"},
    "chat": {"name": "Llama 3", "model": "llama3:latest", "color": "green"},
}

# ===========================
#  FUNCIONES
# ===========================
def run_ollama(model, prompt=None):
    """
    Lanza ollama interactivo o con prompt.
    Devuelve la salida como string.
    """
    try:
        if prompt:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return result.stdout.decode()
        else:
            subprocess.run(["ollama", "run", model])
            return ""
    except FileNotFoundError:
        console.print("[red]Error: ollama no está instalado o no está en el PATH.[/red]")
        sys.exit(1)

def extract_code_block(text):
    """
    Extrae el primer bloque de código entre ```...```
    Devuelve solo el contenido dentro del bloque.
    """
    match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def print_menu():
    table = Table(title="chatllm — menú principal", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Opción", style="bold cyan")
    table.add_column("Descripción")
    table.add_row("1", "Desarrollo (Qwen Coder)")
    table.add_row("2", "Chat general (Llama 3)")
    table.add_row("3", "Salir")
    console.print(table)

def interactive_options():
    raw_opt = Confirm.ask("¿Quieres devolver solo el bloque de código (raw)?", default=False)
    save_opt = Confirm.ask("¿Quieres guardar la salida en un fichero?", default=False)
    filename = None
    if save_opt:
        filename = Prompt.ask("Nombre del fichero")
    return raw_opt, save_opt, filename

# ===========================
#  CLI PRINCIPAL
# ===========================
@click.group(invoke_without_command=True)
@click.argument("prompt", required=False)
@click.option("--model", type=click.Choice(["dev", "chat"]), default=None, help="Selecciona el modelo")
@click.option("--raw", is_flag=True, help="Devuelve solo bloque de código")
@click.option("--output", type=str, help="Guardar la salida en un fichero")
@click.pass_context
def cli(ctx, prompt, model, raw, output):
    console.print(f"[bold blue]{LOGO_MINIMAL}[/bold blue]")

    if prompt and model:
        # prompt directo desde línea de comandos
        m = MODELS[model]
        text = run_ollama(m["model"], prompt)
        if raw:
            text = extract_code_block(text)
        if output:
            with open(output, "w") as f:
                f.write(text)
            console.print(f"[green]Salida guardada en {output}[/green]")
        else:
            console.print(text)
        return

    if ctx.invoked_subcommand is None:
        # Menú interactivo
        print_menu()
        choice = Prompt.ask("Selecciona una opción", choices=["1","2","3"])
        if choice == "3":
            console.print("[yellow]Saliendo...[/yellow]")
            sys.exit(0)

        raw_opt, save_opt, filename = interactive_options()
        prompt_text = Prompt.ask(">>> Dime el código o pregunta")

        if choice == "1":
            ctx.invoke(dev, prompt=prompt_text, raw=raw_opt, output=filename)
        else:
            ctx.invoke(chat, prompt=prompt_text, raw=raw_opt, output=filename)

# ===========================
#  SUBCOMANDOS
# ===========================
@click.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Devuelve solo bloque de código")
@click.option("--output", type=str, help="Guardar la salida en un fichero")
def dev(prompt, raw, output):
    m = MODELS["dev"]
    console.print(f"[bold {m['color']}] {BANNERS['dev']} [/bold {m['color']}]")
    text = run_ollama(m["model"], prompt)
    if raw:
        text = extract_code_block(text)
    if output:
        with open(output, "w") as f:
            f.write(text)
        console.print(f"[green]Salida guardada en {output}[/green]")
    else:
        console.print(text)

@click.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Devuelve solo bloque de código")
@click.option("--output", type=str, help="Guardar la salida en un fichero")
def chat(prompt, raw, output):
    m = MODELS["chat"]
    console.print(f"[bold {m['color']}] {BANNERS['chat']} [/bold {m['color']}]")
    text = run_ollama(m["model"], prompt)
    if raw:
        text = extract_code_block(text)
    if output:
        with open(output, "w") as f:
            f.write(text)
        console.print(f"[green]Salida guardada en {output}[/green]")
    else:
        console.print(text)

cli.add_command(dev)
cli.add_command(chat)

if __name__ == "__main__":
    cli()

