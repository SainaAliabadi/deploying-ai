from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

def log_info(msg: str):
    console.print(f"[bold cyan]INFO[/bold cyan] {msg}")

def log_warn(msg: str):
    console.print(f"[bold yellow]WARN[/bold yellow] {msg}")

def log_err(msg: str):
    console.print(f"[bold red]ERROR[/bold red] {msg}")
