#!/usr/bin/env python3
import click
from .chat import chat
from .dev import dev
from rich.console import Console

console = Console()

LOGO_MINIMAL = r"""
       .__            __  .__  .__           
  ____ |  |__ _____ _/  |_|  | |  |   _____  
_/ ___\|  |  \\__  \\   __\  | |  |  /     \ 
\  \___|   Y  \/ __ \|  | |  |_|  |_|  Y Y  \
 \___  >___|  (____  /__| |____/____/__|_|  /
     \/     \/                     \/ 
"""


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    console.print(f"[bold blue]{LOGO_MINIMAL}[/bold blue]")
    if ctx.invoked_subcommand is None:
        click.echo("Use one of: dev, chat")


cli.add_command(dev)
cli.add_command(chat)

if __name__ == "__main__":
    cli()

