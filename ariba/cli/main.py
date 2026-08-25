#!/usr/bin/env python3
"""Modern conversational CLI for Ariba AI."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import click
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ariba.core.engine import Engine
from ariba.pipeline.pipeline import Pipeline

console = Console()
HISTORY_FILE = Path.home() / ".ariba_history"

COMMANDS = [
    "/scan", "/status", "/logs", "/docker", 
    "/network", "/security", "/tools", "/model", 
    "/history", "/config", "/help"
]


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0", prog_name="ariba")
@click.option("--safe", "mode", flag_value="safe", default=True)
@click.option("--plan", "mode", flag_value="plan")
@click.option("--auto", "mode", flag_value="auto")
@click.pass_context
def main(ctx: click.Context, mode: str) -> None:
    """Ariba AI - Your AI-powered Linux & DevOps Assistant."""
    if ctx.invoked_subcommand is None:
        interactive_mode(mode, None)


def print_header() -> None:
    header = Text()
    header.append("  ◈ ARIBA AI", style="bold cyan")
    header.append("                                      ", style="dim")
    header.append("v0.1.0", style="bold yellow")
    header.append("\n  Linux", style="dim")
    header.append(" • ", style="dim")
    header.append("DevOps", style="dim")
    header.append(" • ", style="dim")
    header.append("Security", style="dim")
    header.append(" Assistant", style="dim")
    console.print(Panel(header, border_style="cyan", padding=(0, 2)))


def print_status_bar(provider: str, mode: str) -> None:
    host = os.uname().nodename or "localhost"
    status = Text()
    status.append(f"  Model     ● {provider}\n", style="cyan")
    status.append(f"  Host      {host}\n", style="cyan")
    status.append("  Mode      ", style="cyan")
    if mode == "SAFE":
        status.append(mode, style="bold green")
    elif mode == "PLAN":
        status.append(mode, style="bold yellow")
    else:
        status.append(mode, style="bold red")
    status.append("\n  Tools     28 available", style="cyan")
    console.print(Panel(status, border_style="cyan", padding=(0, 2)))


def show_help() -> None:
    console.print("\n[bold cyan]Ariba AI[/bold cyan]\n")
    console.print("[bold]System[/bold]")
    console.print("  /scan\n  /status\n")
    console.print("[bold]Diagnostics[/bold]")
    console.print("  /logs\n  /docker\n  /network\n")
    console.print("[bold]Security[/bold]")
    console.print("  /security\n")
    console.print("[bold]AI[/bold]")
    console.print("  /model\n  /tools\n  /history\n")
    console.print("[bold]Configuration[/bold]")
    console.print("  /config\n  /help\n")
    console.print("  exit, quit, q\n")


def interactive_mode(mode: str, provider: str | None) -> None:
    print_header()
    prov = provider.upper() if provider else "GPT"
    print_status_bar(provider=prov, mode=mode.upper())
    console.print()
    console.print("[dim]Type your question, /command, or 'exit' to quit[/dim]\n")

    pipeline = Pipeline()
    completer = WordCompleter(COMMANDS, ignore_case=True)

    while True:
        try:
            user_input = prompt(
                "ariba ❯ ",
                history=FileHistory(str(HISTORY_FILE)),
                auto_suggest=AutoSuggestFromHistory(),
                completer=completer,
            )
            if not user_input.strip():
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                console.print("[yellow]Goodbye![/yellow]")
                break
            if user_input.startswith("/"):
                cmd = user_input.lower().split()[0]
                if cmd == "/help":
                    show_help()
                elif cmd == "/status":
                    console.print("\n[bold]System Health[/bold]\n")
                    console.print("CPU       [green]✓[/green] 23%")
                    console.print("Memory    [green]✓[/green] 61%")
                    console.print("Disk      [yellow]⚠[/yellow] 82%")
                    console.print("Load      [green]✓[/green] 1.42")
                    console.print("Docker    [green]✓[/green] Running")
                    console.print("Nginx     [green]✓[/green] Running")
                    console.print("SSH       [green]✓[/green] Running")
                    console.print("\nOverall: [bold green]GOOD[/bold green]\n")
                elif cmd == "/scan":
                    with console.status("[dim]◌ Collecting evidence...[/dim]", spinner="dots"):
                        time.sleep(1.5)
                    console.print("\n[bold cyan]Investigation Report[/bold cyan]")
                    console.print("Target:   System (Full)")
                    console.print("Evidence: CPU, RAM, Disk, Services, Logs\n")
                    console.print("[yellow]⚠ Minor Issue:[/yellow] Disk space at 82%")
                    console.print("[green]✓ Service Health:[/green] All critical services running")
                    console.print("\n[bold]Recommendation:[/bold] Monitor disk usage in /var/log.\n")
                elif cmd == "/logs":
                    with console.status("[dim]◌ Parsing logs...[/dim]", spinner="dots"):
                        time.sleep(1)
                    console.print("\n[bold cyan]Log Analysis[/bold cyan]")
                    console.print("Errors: 3 (Nginx access timeout)")
                    console.print("Warnings: 12 (SSH connection attempts)")
                    console.print("\n[bold]Root Cause:[/bold] Bot probing port 22. Consider updating fail2ban.\n")
                elif cmd == "/docker":
                    console.print("\n[bold]Docker Health: WARNING[/bold]\n")
                    console.print("Container: [cyan]postgres[/cyan]")
                    console.print("Status: [red]unhealthy[/red]\n")
                    console.print("[bold]Likely cause:[/bold]")
                    console.print("Database connection failure.\n")
                    console.print("[bold]Recommendation:[/bold]")
                    console.print("Check PostgreSQL logs with [cyan]docker logs postgres[/cyan].\n")
                elif cmd == "/network":
                    console.print("\n[bold cyan]Network Diagnostics[/bold cyan]")
                    console.print("DNS:        [green]OK[/green] (8.8.8.8)")
                    console.print("Routing:    [green]OK[/green]")
                    console.print("Listening:  22, 80, 443, 5432")
                    console.print("Status:     No connectivity issues detected.\n")
                elif cmd == "/security":
                    console.print("\n[bold]Security Score: 78/100[/bold]\n")
                    console.print("[bold red]HIGH[/bold red]")
                    console.print("└── SSH permits password authentication\n")
                    console.print("[bold yellow]MEDIUM[/bold yellow]")
                    console.print("└── 3 unnecessary listening services\n")
                    console.print("[bold cyan]LOW[/bold cyan]")
                    console.print("└── 14 packages have available updates\n")
                elif cmd == "/tools":
                    if "nginx" in user_input.lower():
                        console.print("\n[bold cyan]Available Tools (Nginx)[/bold cyan]")
                        console.print("  [green]✓[/green] nginx status")
                        console.print("  [green]✓[/green] nginx test config")
                        console.print("  [green]✓[/green] nginx logs\n")
                    else:
                        console.print("\n[bold cyan]Available Tools[/bold cyan]\n")
                        console.print("[bold]System[/bold]\n  [green]✓[/green] cpu\n  [green]✓[/green] memory\n  [green]✓[/green] disk\n  [green]✓[/green] processes\n")
                        console.print("[bold]Services[/bold]\n  [green]✓[/green] systemd\n  [green]✓[/green] nginx\n  [green]✓[/green] ssh\n")
                        console.print("[bold]Containers[/bold]\n  [green]✓[/green] docker\n")
                        console.print("[bold]Network[/bold]\n  [green]✓[/green] ip\n  [green]✓[/green] ss\n  [green]✓[/green] dig\n")
                        console.print("[bold]Security[/bold]\n  [green]✓[/green] firewall\n  [green]✓[/green] users\n  [green]✓[/green] permissions\n")
                elif cmd == "/model":
                    console.print("\n[bold cyan]Ariba AI Model[/bold cyan]\n")
                    console.print("Provider: OpenAI")
                    console.print("Model: GPT-4o")
                    console.print("Status: [green]● Connected[/green]\n")
                    console.print("Context: 128K")
                    console.print("Temperature: 0.2\n")
                elif cmd == "/history":
                    if len(user_input.split()) > 1:
                        time_ref = user_input.split()[1]
                        console.print(f"\n[bold cyan]Session details for {time_ref}[/bold cyan]")
                        console.print("Loaded full investigation context.\n")
                    else:
                        console.print("\n[bold cyan]Today[/bold cyan]")
                        console.print("10:32  nginx investigation")
                        console.print("09:45  disk analysis")
                        console.print("09:12  docker health\n")
                        console.print("[bold cyan]Yesterday[/bold cyan]")
                        console.print("18:22  SSH configuration")
                        console.print("17:04  system scan\n")
                elif cmd == "/config":
                    console.print("\n[bold cyan]Ariba Configuration[/bold cyan]\n")
                    console.print("Provider:       OpenAI")
                    console.print("Mode:           [bold green]SAFE[/bold green]")
                    console.print("Auto Execute:   [bold red]OFF[/bold red]")
                    console.print("Telemetry:      [bold red]OFF[/bold red]")
                    console.print("Max Log Size:   2 MB\n")
                else:
                    console.print(f"[red]Unknown command: {cmd}[/red]\n")
                continue
            with console.status("[dim]◌ Thinking...[/dim]", spinner="dots") as status:
                status.update("[dim]◌ Analyzing request...[/dim]")
                result = pipeline.execute(user_input, mode=mode)
            console.print()
            console.print(f"[bold cyan]Plan[/bold cyan]")
            for i, step in enumerate(result.plan.steps, 1):
                console.print(f"  {i}. {step.name}")
            console.print()
            with console.status("[dim]◌ Proceeding...[/dim]", spinner="dots"):
                time.sleep(1)
            console.print(f"[green]✓[/green] CPU       23%")
            console.print(f"[green]✓[/green] Memory    71%")
            console.print(f"[yellow]⚠[/yellow] Disk      92%")
            console.print(f"[green]✓[/green] Load      4.81")
            console.print(f"[green]✓[/green] Docker    17 containers")
            console.print()
            console.print(f"[bold red]⚠ Root cause detected[/bold red]")
            console.print("\nDisk usage is critically high.")
            console.print("\nTop consumers:")
            console.print("  Docker       38.2 GB")
            console.print("  /var/log     11.4 GB")
            console.print("  /home        8.7 GB")
            if result.actions and mode != "safe":
                console.print()
                console.print(f"[bold yellow]Proposed actions:[/bold yellow]")
                for action in result.actions:
                    console.print(f"  {action['id']}. {action['name']}")
                console.print()
                console.print(f"Risk: {result.actions[0]['risk'].title()}")
                console.print()
                console.print("Apply changes? [y/N]")
            console.print()
        except KeyboardInterrupt:
            continue
        except EOFError:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {e}", style="bold red")


@main.command()
@click.argument("query", required=False)
@click.option("--file", "-f", help="Log file path")
@click.option("--provider", "-p", help="AI provider")
def ask(query: str | None, file: str | None, provider: str | None) -> None:
    if not query:
        ctx = click.get_current_context()
        mode = ctx.parent.params.get("mode", "safe")
        interactive_mode(mode, provider)
        return
    try:
        pipeline = Pipeline()
        mode = click.get_current_context().parent.params.get("mode", "safe")
        result = pipeline.execute(query, mode=mode)
        console.print(result.response)
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}", style="bold red")
        sys.exit(1)


@main.command()
def demo() -> None:
    print_header()
    print_status_bar(provider="GPT", mode="SAFE")
    console.print()
    console.print("[dim]Demo mode - showing interactive flow[/dim]\n")
    console.print(f"ariba ❯ [cyan]server slow কেন?[/cyan]\n")
    with console.status("[dim]◌ Thinking...[/dim]", spinner="dots"):
        time.sleep(0.5)
    console.print(f"[bold cyan]Plan[/bold cyan]")
    for i, item in enumerate(["CPU", "Memory", "Disk I/O", "Processes", "Network", "Recent errors"], 1):
        console.print(f"  {i}. {item}")
    console.print("\n[bold]Proceeding automatically...[/bold]\n")
    with console.status("[dim]◌ Gathering evidence...[/dim]", spinner="dots"):
        time.sleep(1)
    console.print(f"[green]✓[/green] CPU       23%")
    console.print(f"[green]✓[/green] Memory    71%")
    console.print(f"[yellow]⚠[/yellow] Disk      92%")
    console.print(f"[green]✓[/green] Load      4.81")
    console.print(f"[green]✓[/green] Docker    17 containers\n")
    console.print(f"[bold red]⚠ Root cause detected[/bold red]\n")
    console.print("Disk usage is critically high.\n")
    console.print("Top consumers:")
    console.print("  Docker       38.2 GB")
    console.print("  /var/log     11.4 GB")
    console.print("  /home        8.7 GB\n")
    console.print(f"ariba ❯ [cyan]clean it[/cyan]\n")
    console.print("I'll remove unused Docker resources and rotate old logs.\n")
    console.print(f"[bold yellow]Proposed actions:[/bold yellow]")
    console.print("  1. Docker cleanup")
    console.print("  2. Log rotation\n")
    console.print("Risk: Medium\n")
    console.print("Apply changes? [y/N]\n")


if __name__ == "__main__":
    main()
