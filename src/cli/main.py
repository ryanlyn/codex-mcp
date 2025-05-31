#!/usr/bin/env python3
"""Codex CLI tool."""

import typer
from rich.console import Console
from rich.panel import Panel

from ..browser import DEFAULT_CDP_PORT, BrowserConnection, get_default_launch_command

app = typer.Typer(
    name="codex-cli",
    help="OpenAI Codex CLI tool",
    add_completion=False,
)
console = Console()


@app.command()
def test(
    port: int = typer.Option(DEFAULT_CDP_PORT, "--port", "-p", help="Chrome DevTools Protocol port"),
):
    """Test browser connection."""
    console.print(f"[bold]Testing browser connection on port {port}...[/bold]")

    browser = BrowserConnection(port=port)

    if browser.test_connection_sync():
        console.print(f"[green]✓[/green] Successfully connected to Chrome DevTools Protocol on port {port}")
        console.print("[green]✓[/green] Browser connection test passed!")
    else:
        console.print(f"[red]✗[/red] Cannot connect to Chrome DevTools Protocol on port {port}")
        console.print("\n[yellow]Please start Chrome with remote debugging enabled:[/yellow]")

        launch_cmd = get_default_launch_command()
        console.print(Panel(launch_cmd, title="Run this command", border_style="yellow", padding=(1, 2)))

        console.print("\n[dim]Note: Make sure all Chrome instances are closed before running this command.[/dim]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
