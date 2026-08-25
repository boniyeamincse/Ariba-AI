# Ariba AI

> **Your AI-powered Linux & DevOps Assistant**

Ariba AI is a command-line tool that helps you diagnose, analyze, and troubleshoot Linux systems and DevOps workflows using natural language. It combines system data collection with AI-powered insights to give you actionable answers fast.

```bash
# Interactive mode (recommended)
ariba
ariba ❯ nginx error দেখো

# Single query mode
ariba ask "docker কেন কাজ করছে না?"
ariba ask "disk space check করো"
ariba ask "server slow কেন?"
ariba ask "ssh configuration check করো"
ariba ask "এই logটা analyze করো"

# Demo mode (no API key needed)
ariba demo
```

## Features (MVP — v0.1)

- **Natural-language CLI** — ask questions in plain English or Bangla
- **Linux system diagnostics** — CPU, memory, disk, uptime, and more
- **Log analysis** — read and summarize common log files
- **Nginx diagnostics** — inspect configs, errors, and status
- **Docker diagnostics** — container health, images, and networks
- **AI API integration** — OpenAI, Gemini, Claude, and Ollama support
- **Read-only by default** — safe exploration without side effects
- **Command approval** — optional execution of suggested commands

## Roadmap

- **v0.2** — Extended DevOps tooling (Kubernetes, Terraform, CI/CD)
- **v0.3** — Security & SOC features (audit, intrusion detection, compliance)
- **Future** — Full **Ariba AI Linux** environment

## Installation

```bash
# Clone the repository
git clone https://github.com/ariba-ai/ariba.git
cd ariba

# Install in editable mode
pip install -e .

# Optional: install AI provider support
pip install -e ".[openai,gemini,claude,ollama]"
```

## Quick Start

```bash
# Set your AI API key (example for OpenAI)
export OPENAI_API_KEY="sk-..."

# Start interactive conversational mode (modern TUI)
ariba

# Ask a single question
ariba ask "disk space check করো"

# Analyze a log file
ariba ask "এই logটা analyze করো --file /var/log/syslog"

# Run demo (no API key required)
ariba demo
```

## Project Structure

```
ariba/
├── cli/          # Command-line interface (Click)
├── core/         # Orchestration, intent parsing, and response generation
├── collectors/   # System data collectors (system, logs, network, docker, services)
├── providers/    # AI provider integrations (OpenAI, Gemini, Claude, Ollama)
├── security/     # Command safety, approval, and read-only enforcement
├── renderer/     # Output formatting (tables, colors, markdown)
tests/            # Unit and integration tests
docs/             # Documentation
```

## Configuration

Ariba AI can be configured via environment variables or a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `ARIBA_AI_PROVIDER` | AI provider to use | `openai` |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `GEMINI_API_KEY` | Google Gemini API key | — |
| `ANTHROPIC_API_KEY` | Claude API key | — |
| `ARIBA_OLLAMA_HOST` | Ollama host | `http://localhost:11434` |
| `ARIBA_READ_ONLY` | Enforce read-only mode | `true` |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black ariba tests

# Lint
ruff check ariba tests
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Trademark Note

Before releasing publicly, please verify GitHub availability, domain registration, and any existing trademark or name usage for **"Ariba AI"**.

---

Built with ❤️ for Linux administrators, DevOps engineers, and SREs.
# Ariba-AI
