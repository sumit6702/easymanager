import os
import yaml
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

app = typer.Typer()
console = Console()

CONFIG_FILE = "configdots.yml"
DOTFILES_DIR = "dotfiles"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return []
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f) or []


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(config, f)


def update_status(name, status):
    config = load_config()
    for entry in config:
        if entry["name"] == name:
            entry["status"] = status
    save_config(config)


def get_entry(name):
    return next((entry for entry in load_config() if entry["name"] == name), None)


@app.command()
def list():
    """List all dotfiles with their status."""
    config = load_config()
    table = Table(title="EasyDots", show_header=True, header_style="bold magenta")
    table.add_column("No.", style="blue")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Target", style="green")
    table.add_column("Status", style="yellow")

    for entry in config:
        table.add_row(
            str(config.index(entry) + 1),
            entry["name"],
            entry["source"],
            entry["target"],
            entry["status"],
        )

    console.print(table)


@app.command()
def link(
    name: str = typer.Option(None, "-n", "--name", help="Name of the dotfile to link"),
    all: bool = typer.Option(False, "-a", "--all", help="Link all dotfiles"),
):
    """Symlink dotfiles based on config."""
    if not name and not all:
        console.print(
            "[red]Please specify a dotfile name using --name or use -a to link all dotfiles.[/red]"
        )
        return

    config = load_config()
    for entry in config:
        if name and entry["name"] != name:
            continue
        src = Path(entry["source"]).expanduser()
        dest = Path(entry["target"]).expanduser()
        if dest.exists() and not dest.is_symlink():
            backup = dest.with_suffix(".bak")
            dest.replace(backup)
            console.print(f"[yellow]Backed up {dest} -> {backup}[/yellow]")
            dest.symlink_to(src)
            update_status(entry["name"], "Linked")
            console.print(f"[green]Linked {entry['name']} -> {dest}[/green]")
        elif dest.is_symlink():
            console.print(f"[blue]Skipping {entry['name']}, already linked.[/blue]")
        else:
            dest.symlink_to(src)
            update_status(entry["name"], "Linked")
            console.print(f"[green]Linked {entry['name']} -> {dest}[/green]")


@app.command()
def unlink(
    name: str = typer.Option(
        None, "-n", "--name", help="Name of the dotfile to unlink"
    ),
    all: bool = typer.Option(False, "-a", "--all", help="Unlink all dotfiles"),
):
    if not name and not all:
        console.print(
            "[red]Please specify a dotfile name using --name or use -a to unlink all dotfiles.[/red]"
        )
        return

    config = load_config()
    for entry in config:
        if name and entry["name"] != name:
            continue
        dest = Path(entry["target"]).expanduser()
        if dest.is_symlink():
            dest.unlink()
            update_status(entry["name"], "Unlinked")
            console.print(f"[red]Unlinked {entry['name']}[/red]")
        else:
            console.print(f"[blue]Skipping {entry['name']}, not a symlink.[/blue]")


@app.command()
def add(name: str, source: str, target: str):
    """Add a new dotfile entry."""
    config = load_config()
    if any(entry["name"] == name for entry in config):
        console.print("[red]Dotfile with this name already exists![/red]")
        return
    config.append(
        {"name": name, "source": source, "target": target, "status": "Unlinked"}
    )
    save_config(config)
    console.print(f"[green]Added {name} to config.[/green]")


@app.command()
def remove(name: str):
    """Remove a dotfile entry."""
    config = load_config()
    if not any(entry["name"] == name for entry in config):
        console.print(f"[red]Dotfile {name} not found![/red]")
        return
    confirm = Confirm.ask(f"Are you sure you want to remove {name}?")
    if confirm:
        config = [entry for entry in config if entry["name"] != name]
        save_config(config)
        console.print(f"[red]Removed {name} from config.[/red]")


if __name__ == "__main__":
    app()
