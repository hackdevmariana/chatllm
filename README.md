# chatllm

`chatllm` is a lightweight command-line interface for interacting with local Ollama models.  
It provides a simple menu, model selection, and optional direct prompts.  
The tool is designed to be installed globally using `pipx`.

## Features

- Menu for selecting different Ollama models
- Direct prompt mode (`chatllm "Your question"`)
- Subcommands for specific roles (development, general chat)
- Clean console interface using Rich and Click
- Fully local and does not require external APIs

## Requirements

- Python 3.10 or later
- `pipx` installed
- Ollama installed and running locally
- At least two models available (for example `qwen2.5-coder:7b` and `llama3:latest`)

## Installation

### Install using pipx from GitHub

```
pipx install git+https://github.com/hackdevmariana/chatllm
```

### Local installation for development

Clone the repository:

```
git clone https://github.com/hackdevmariana/chatllm
cd chatllm
pipx install .
```

To update:

```
git pull
pipx reinstall .
```

## Usage

### Run the main menu

```
chatllm
```

### Development mode

```
chatllm dev
```

### General chat mode

```
chatllm chat
```

### Direct prompt without entering the menu

```
chatllm "Explain async in Python"
```

### Direct prompt in a specific mode

```
chatllm dev "Write a function that parses a CSV file"
```

## Uninstall

```
pipx uninstall chatllm
```


