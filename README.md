# AI Tool-Using Agent

A local learning project using LangChain, LangGraph, and Ollama.

## Features
- Calculator, local time, web search, and public API tools
- LangGraph state and conditional tool-routing loop
- SQLite conversation history (simple long-term storage)
- Sequential and parallel tool examples
- Supervisor-style multi-agent routing demo
- Iteration limits, tool error handling, and request timeouts

## Requirements
- Python 3.11+ recommended
- Ollama installed and running
- An Ollama model available locally (default: `llama3.2:1b`)
- Internet access for web search and the public API tool

## Setup (Windows PowerShell)

```powershell
cd "C:\Users\Aadi Rhythm\Documents\LYFnGo\AI_Tool_Using_Agent"
python -m venv .venv
Set-ExecutionPolicy -Scope Process RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
ollama pull llama3.2:1b
```

If your virtual environment already exists, do not recreate it; activate it and install requirements.

Copy `.env.example` to `.env` if you want to customize settings. Never commit `.env`.

## Run

```powershell
python main.py
```

Try:
- `Multiply 67 by 89.`
- `What time is it?`
- `Search the web for Python 3.14 release information.`
- `Suggest an activity using the public API.`
- `Remember that my preferred editor is VS Code.`
- `What editor did I ask you to remember?`

Type `exit` to quit.

## Other demos

```powershell
python demos\multi_agent_patterns.py
python demos\async_tools_demo.py
```

The demos are learning examples; the main app is the LangGraph tool-using agent.

## GitHub upload

1. Create an empty repository on GitHub, for example `AI_Tool_Using_Agent`.
2. Do not add a README/license/gitignore on GitHub if this local folder already has those files.
3. In the project terminal:

```powershell
git init
git add .
git status
git commit -m "Build LangGraph tool-using AI agent"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/AI_Tool_Using_Agent.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME` with your GitHub username. If `git remote add origin` says origin already exists, inspect it with `git remote -v` and update it only if needed:
`git remote set-url origin https://github.com/YOUR-GITHUB-USERNAME/AI_Tool_Using_Agent.git`

Before committing, verify `.env` is not staged:
`git status`
