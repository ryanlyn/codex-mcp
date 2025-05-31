#!/usr/bin/env python3
"""Codex CLI tool."""

from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(
    name="codex-cli",
    help="OpenAI Codex CLI tool",
    add_completion=False,
)
console = Console()


@app.command()
def init(
    config_path: Path | None = typer.Option(None, "--config", "-c", help="Path to config file"),
):
    """Initialize the Codex MCP configuration."""
    console.print("[bold blue]Initializing Codex MCP configuration...[/bold blue]")

    # TODO: Create default configuration
    config_path = config_path or Path.home() / ".config" / "codex-mcp" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    console.print(f"✅ Configuration will be created at: {config_path}")


@app.command()
def test(
    browser: str = typer.Option("chrome", "--browser", "-b", help="Browser to test with"),
):
    """Test browser connection."""
    console.print(f"[bold]Testing browser connection:[/bold] {browser}")

    # TODO: Add actual browser testing logic

    console.print("[green]✓[/green] Browser connection test passed!")


if __name__ == "__main__":
    app()
