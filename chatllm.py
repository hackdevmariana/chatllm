#!/usr/bin/env python3
import click
import subprocess
import sys
import re
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
 \___| >___|  (____  /__| |____/____/__|_|  /
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
def run_ollama(model, prompt=None, raw=False, output=None, show_banner=True):
    """
    Lanza Ollama y captura la salida.
    Si raw=True, devuelve solo el primer bloque de código.
    Si output se indica, guarda la salida en el fichero indicado.
    """
    try:
        if prompt:
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output_text = result.stdout.decode()

            if raw:
                match = re.search(r"```(?:\w+)?\n(.*?)```", output_text, re.DOTALL)
                if match:
                    output_text = match.group(1).strip()

            if output:
                with open(output, "w") as f:
                    f.write(output_text)
            else:
                if show_banner:
                    console.print(output_text)
                else:
                    # Si no queremos banner, imprimimos plano
                    print(output_text)
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
@click.argument("prompt", required=False)
@click.option("--model", type=click.Choice(["dev", "chat"]), help="Selecciona el modelo")
@click.option("--raw", is_flag=True, help="Devuelve solo el bloque de código")
@click.option("--output", type=click.Path(), help="Guardar salida en fichero")
@click.pass_context
def cli(ctx, prompt, model, raw, output):
    """
    Entrada principal. Si se pasa un prompt directo, entra en modo rápido.
    """
    if not raw:
        console.print(f"[bold blue]{LOGO_MINIMAL}[/bold blue]")

    if prompt and model:
        m = MODELS[model]
        if not raw:
            console.print(f"[bold {m['color']}]Prompt directo detectado para {model}[/bold {m['color']}]")
        run_ollama(m["model"], prompt=prompt, raw=raw, output=output, show_banner=not raw)
        return

    if ctx.invoked_subcommand is None:
        print_menu()
        choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3"])

        if choice == "1":
            ctx.invoke(dev, raw=raw, output=output)
        elif choice == "2":
            ctx.invoke(chat, raw=raw, output=output)
        else:
            console.print("[yellow]Saliendo...[/yellow]")
            sys.exit(0)

# ===========================
#  SUBCOMANDOS
# ===========================
@cli.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Devuelve solo el bloque de código")
@click.option("--output", type=click.Path(), help="Guardar salida en fichero")
def dev(prompt, raw, output):
    """Modo desarrollo (Qwen Coder)."""
    m = MODELS["dev"]
    if not raw:
        console.print(f"[bold {m['color']}] {BANNERS['dev']} [/bold {m['color']}]")
    run_ollama(m["model"], prompt=prompt, raw=raw, output=output, show_banner=not raw)

@cli.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Devuelve solo el bloque de código")
@click.option("--output", type=click.Path(), help="Guardar salida en fichero")
def chat(prompt, raw, output):
    """Modo chat general (Llama 3)."""
    m = MODELS["chat"]
    if not raw:
        console.print(f"[bold {m['color']}] {BANNERS['chat']} [/bold {m['color']}]")
    run_ollama(m["model"], prompt=prompt, raw=raw, output=output, show_banner=not raw)

if __name__ == "__main__":
    cli()

