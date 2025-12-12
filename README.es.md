`chatllm` es una herramienta de línea de comandos para interactuar con modelos locales de Ollama.  
Incluye un menú sencillo, selección de modelos y soporte para pasar un prompt directo.  
Está diseñado para instalarse globalmente mediante `pipx`.

## Características

- Menú para seleccionar diferentes modelos de Ollama
- Modo de prompt directo (`chatllm "Tu pregunta"`)
- Subcomandos para distintos usos (desarrollo, chat general)
- Interfaz de consola limpia utilizando Rich y Click
- Funciona completamente en local sin API externas

## Requisitos

- Python 3.10 o superior
- `pipx` instalado
- Ollama instalado y funcionando de forma local
- Al menos dos modelos disponibles (por ejemplo `qwen2.5-coder:7b` y `llama3:latest`)

## Instalación

### Instalación con pipx desde GitHub

```
pipx install git+https://github.com/hackdevmariana/chatllm
```

### Instalación local para desarrollo

Clonar el repositorio:

```
git clone https://github.com/hackdevmariana/chatllm
cd chatllm
pipx install .
```

Para actualizar:

```
git pull
pipx reinstall .
```

## Uso

### Ejecutar el menú principal

```
chatllm
```

### Modo de desarrollo

```
chatllm dev
```

### Modo de chat general

```
chatllm chat
```

### Prompt directo sin entrar al menú

```
chatllm "Háblame de las f-strings en Python"
```

### Prompt directo en modo específico

```
chatllm dev "Genera una función en Python que lea un archivo CSV"
```

## Desinstalación

```
pipx uninstall chatllm
```


