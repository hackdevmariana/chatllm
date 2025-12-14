import json
import subprocess
from pathlib import Path

BASE_DIR = Path.home() / ".local" / "share" / "chatllm"
BASE_DIR.mkdir(parents=True, exist_ok=True)


# ---------- sesiones ----------

def session_dir(mode: str) -> Path:
    d = BASE_DIR / mode
    d.mkdir(exist_ok=True)
    return d


def session_file(mode: str, session: str) -> Path:
    return session_dir(mode) / f"{session}.json"


def list_sessions(mode: str) -> list[str]:
    return [f.stem for f in session_dir(mode).glob("*.json")]


# ---------- historial ----------

def load_history(mode: str, session: str) -> list[dict]:
    file = session_file(mode, session)
    if not file.exists():
        return []
    try:
        return json.loads(file.read_text())
    except json.JSONDecodeError:
        return []


def save_history(mode: str, session: str, history: list[dict]) -> None:
    session_file(mode, session).write_text(
        json.dumps(history, indent=2, ensure_ascii=False)
    )


def append_message(mode: str, session: str, role: str, content: str) -> None:
    history = load_history(mode, session)
    history.append({"role": role, "content": content})
    save_history(mode, session, history)


def clear_history(mode: str, session: str) -> None:
    session_file(mode, session).unlink(missing_ok=True)


# ---------- ejecución ollama ----------

def run_ollama(model: str, messages: list[dict]) -> str:
    prompt = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in messages
    ) + "\nAssistant:"

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return result.stdout.decode().strip()

