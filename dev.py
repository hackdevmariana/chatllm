import click
from common import MODELS, BANNERS, run_ollama, extract_code_block, console


@click.command()
@click.argument("prompt", required=False)
@click.option("--raw", is_flag=True, help="Return only code block")
@click.option("--output", type=str, help="Save output to file")
def dev(prompt, raw, output):
    """Development mode (code generation)."""
    m = MODELS["dev"]

    console.print(f"[bold {m['color']}]{BANNERS['dev']}[/bold {m['color']}]")

    if not prompt:
        prompt = click.prompt(">>> Describe the code you want")

    text = run_ollama(m["model"], prompt)

    if raw:
        text = extract_code_block(text)

    if output:
        with open(output, "w") as f:
            f.write(text)
        console.print(f"[green]Saved to {output}[/green]")
    else:
        console.print(text)


