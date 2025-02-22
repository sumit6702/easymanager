import os
import yaml
import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm

app = typer.Typer()
console = Console()

SCRIPT_FILE = "scripts.yml"


def load_scripts():
    if not os.path.exists(SCRIPT_FILE):
        return []
    with open(SCRIPT_FILE, "r") as f:
        return yaml.safe_load(f) or []


def save_scripts(scripts):
    with open(SCRIPT_FILE, "w") as f:
        yaml.safe_dump(scripts, f)


@app.command()
def run():
    """Select and run a script interactively."""
    scripts = load_scripts()
    if not scripts:
        console.print("[red]No scripts found.[/red]")
        return

    # Display scripts in a numbered table
    table = Table(
        title="Select a Script to Run", show_header=True, header_style="bold magenta"
    )
    table.add_column("No.", style="blue", justify="right")
    table.add_column("Script", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")

    for index, script in enumerate(scripts, start=1):
        table.add_row(str(index), script["name"], script["source"])

    console.print(table)

    # Prompt for user selection
    while True:
        try:
            choice = int(
                console.input(
                    "[bold green]Enter script number to run (0 to cancel): [/bold green]"
                )
            )
            if choice == 0:
                console.print("[yellow]Cancelled.[/yellow]")
                return
            if 1 <= choice <= len(scripts):
                break
            else:
                console.print("[red]Invalid choice, please enter a valid number.[/red]")
        except ValueError:
            console.print("[red]Invalid input, enter a number.[/red]")

    # Execute the selected script
    selected_script = scripts[choice - 1]
    console.print(f"[green]Running script: {selected_script['name']}[/green]")
    os.system(f"bash \"{selected_script['source']}\"")
    update_status(selected_script["name"], "Executed")
    console.print(f"[blue]Script executed: {selected_script['name']}[/blue]")


@app.command()
def delete(name: str):
    """Delete a script entry from the list."""
    scripts = load_scripts()
    if not any(entry["name"] == name for entry in scripts):
        console.print(f"[red]Script not found: {name}[/red]")
        raise typer.Exit(code=1)

    if Confirm.ask(f"Are you sure you want to delete {name}?"):
        scripts = [entry for entry in scripts if entry["name"] != name]
        save_scripts(scripts)
        console.print(f"[green]Script deleted: {name}[/green]")


if __name__ == "__main__":
    app()
