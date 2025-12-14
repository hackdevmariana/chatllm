import json
import subprocess
from pathlib import Path
from typing import List, Dict

# ===========================
#  RUTAS Y DIRECTORIOS
# ===========================

DATA_DIR = Path.home() / ".local" / "share" / "chatllm"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ===========================
#  HISTORIAL
# ===========================

def history_file(mode: str) -> Path:
    """
    Devuelve la ruta del fichero de historial para un modo dado.
    """
    return DATA_DIR / f"{mode}_history.json"


def load_history(mode: str) -> List[Dict[str, str]]:
    """
    Carga el historial desde disco.
    """
    file = history_file(mode)
    if not file.exists():
        return []

    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_history(mode: str, history: List[Dict[str, str]]) -> None:
    """
    Guarda el historial en disco.
    """
    history_file(mode).write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def append_message(mode: str, role: str, content: str) -> None:
    """
    Añade un mensaje al historial.
    """
    history = load_history(mode)
    history.append({"role": role, "content": content})
    save_history(mode, history)


def clear_history(mode: str) -> None:
    """
    Borra el historial.
    """
    history_file(mode).unlink(missing_ok=True)

# ===========================
#  OLLAMA
# ===========================

def run_ollama(model: str, messages: List[Dict[str, str]]) -> str:
    """
    Ejecuta Ollama con contexto (historial).
    """
    prompt = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in messages
    ) + "\nAssistant:"

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return result.stdout.decode("utf-8").strip()

