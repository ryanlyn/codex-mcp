#!/usr/bin/env python3

import asyncio

import typer
from rich.console import Console
from rich.panel import Panel

from ..agent import CodexAgent
from ..browser import DEFAULT_CDP_PORT, BrowserConnection, get_default_launch_command

app = typer.Typer(
    name="codex-cli",
    help="OpenAI Codex CLI tool",
    add_completion=False,
)
console = Console()


async def ensure_browser_connection(browser: BrowserConnection, port: int) -> None:
    if not await browser.test_connection(force=True):
        console.print(f"[red]✗[/red] Cannot connect to Chrome DevTools Protocol on port {port}")
        console.print("\n[yellow]Please start Chrome with remote debugging enabled:[/yellow]")

        launch_cmd = get_default_launch_command()
        console.print(Panel(launch_cmd, title="Run this command", border_style="yellow", padding=(1, 2)))

        console.print("\n[dim]Note: Make sure all Chrome instances are closed before running this command.[/dim]")
        raise typer.Exit(1)


@app.command()
def check(
    port: int = typer.Option(DEFAULT_CDP_PORT, "--port", "-p", help="Chrome DevTools Protocol port"),
):
    asyncio.run(check_async(port))


async def check_async(
    port: int = DEFAULT_CDP_PORT,
):
    console.print(f"[bold]Testing browser connection on port {port}...[/bold]")

    browser = BrowserConnection(port=port)

    await ensure_browser_connection(browser, port)

    console.print(f"[green]✓[/green] Successfully connected to Chrome DevTools Protocol on port {port}")
    console.print("[green]✓[/green] Browser connection test passed!")

    codex_agent = CodexAgent(browser_connection=browser)
    result = await codex_agent.wait_until_logged_in()
    console.print(result)


@app.command()
def do(
    instruction: str = typer.Argument(..., help="Natural language instruction to execute on Codex"),
    port: int = typer.Option(DEFAULT_CDP_PORT, "--port", "-p", help="Chrome DevTools Protocol port"),
):
    asyncio.run(do_async(instruction, port))


async def do_async(instruction: str, port: int = DEFAULT_CDP_PORT):
    browser = BrowserConnection(port=port)
    await ensure_browser_connection(browser, port)

    console.print(f"[bold]Executing: {instruction}[/bold]\n")

    codex_agent = CodexAgent(browser_connection=browser)

    console.print("[dim]Checking login status...[/dim]")
    await codex_agent.wait_until_logged_in()

    console.print("[yellow]Processing instruction...[/yellow]")
    result = await codex_agent.execute_instruction(instruction)

    console.print("\n[green]✓[/green] Task completed successfully!")
    console.print(Panel(result, title="Result", border_style="green", padding=(1, 2)))


if __name__ == "__main__":
    app()
