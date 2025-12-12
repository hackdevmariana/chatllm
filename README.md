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

### Direct prompt with raw output

Returns only the code block, ready to copy or redirect:

```
chatllm --model dev --raw "Write a Python script that prints 'Hello World'"
```

Example redirect to file:

```
chatllm --model dev --raw "Write a Python script that prints 'Hello World'" > hello.py
```

### Interactive options in the menu

When using the menu, you can choose:

- Whether to return only the raw code block
- Whether to save the output directly to a file and provide the filename

## Uninstall

```
pipx uninstall chatllm
```


