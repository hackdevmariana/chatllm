import subprocess
import sys
import re
from rich.console import Console

console = Console()

MODELS = {
    "dev": {
        "name": "Qwen 2.5 Coder",
        "model": "qwen2.5-coder:7b",
        "color": "cyan",
    },
    "chat": {
        "name": "Llama 3",
        "model": "llama3:latest",
        "color": "green",
    },
}

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
""",
}


def run_ollama(model, prompt=None):
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
        console.print("[red]Error: ollama not found in PATH[/red]")
        sys.exit(1)


def extract_code_block(text):
    match = re.search(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

