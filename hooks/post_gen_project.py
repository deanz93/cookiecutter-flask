from pathlib import Path
import shutil
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table
from alive_progress import alive_bar


console = Console()

# ✅ Success & Warning messages
SUCCESS = "[bold green]✅ SUCCESS:[/bold green]"
WARNING = "[bold yellow]⚠️ WARNING:[/bold yellow]"
INFO = "[bold blue]ℹ️ INFO:[/bold blue]"

# 🔥 Custom ASCII Art for Branding (P L I S C A)
ASCII_ART = r"""
 _____  _      _____  _____  _____          
|  __ \| |    |_   _|/ ____|/ ____|   /\    
| |__) | |      | | | (___ | |       /  \   
|  ___/| |      | |  \___ \| |      / /\ \  
| |    | |____ _| |_ ____) | |____ / ____ \ 
|_|    |______|_____|_____/ \_____/_/    \_\
"""

# 🚀 Welcome Panel
def show_welcome_message():
    """Displays a centered welcome message with spacing."""
    console.print("\n" + ASCII_ART.center(console.width), style="bold magenta")
    
    console.print("\n")
    console.print(
        Panel(
            "[bold cyan]🚀 Welcome to the Flask Boilerplate Generator![/bold cyan]\n\n"
            "[green]This setup will guide you through initializing your project.[/green]",
            title="🛠️ [bold magenta]Flask Boilerplate Installer[/bold magenta]",
            expand=False,
            padding=(1, 4),  # Add more margin around the text
        )
    )
    console.print("\n")


# 🗑️ Removing Unnecessary Files with Animated Progress
def remove_unnecessary_files():
    """Removes unwanted files based on project settings with animation."""
    files_to_remove = []

    # Open source cleanup
    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        files_to_remove += ["CONTRIBUTORS.md", "LICENSE"]

    # GPLv3 cleanup
    if "{{ cookiecutter.open_source_license }}" != "GPLv3":
        files_to_remove.append("COPYING")

    # Docker files cleanup
    if "{{ cookiecutter.use_docker }}".lower() == "n":
        files_to_remove += [
            "docker-compose.local.yml",
            ".dockerignore",
            "Dockerfile",
            "entrypoint.sh",
            "Makefile",
        ]
        if Path("compose").exists():
            shutil.rmtree("compose")

    console.print("\n🗑️ [bold yellow]Cleaning up unnecessary files...[/bold yellow]\n")
    
    with alive_bar(len(files_to_remove), title="Processing Files...", bar="smooth") as bar:
        for file in files_to_remove:
            path = Path(file)
            if path.exists():
                path.unlink()
                console.print(f"{INFO} Removed {file}")
            bar()
    
    console.print("\n")


# 📂 Copy .env File with a Status Update
def copy_env_file():
    """Copies .env.example to .env with a formatted message."""
    console.print("\n📂 [bold cyan]Setting up environment variables...[/bold cyan]\n")

    if Path(".env.example").exists():
        shutil.copy(".env.example", ".env")
        console.print(f"{INFO} Copied .env.example to .env")
    else:
        console.print(f"{WARNING} .env.example not found! Please create a .env file manually.")

    console.print("\n")


# 🏆 Next Steps in a Beautiful Table
def show_next_steps():
    """Displays next steps in a structured format with spacing."""
    console.print("\n💡 [bold yellow]Next Steps[/bold yellow]\n")

    table = Table(expand=False, padding=(0, 3))
    table.add_column("#", justify="center", style="cyan", no_wrap=True)
    table.add_column("Action", style="bold green")

    table.add_row("📂", "Navigate into your project directory")
    table.add_row("🐍", "Run `pip install -r requirements.txt` to install dependencies")
    table.add_row("🚀", "Start your project with `flask run`")

    console.print(table)
    console.print("\n")


# 🎉 Final Celebration Animation
def celebration_animation():
    """Simulates a smooth completion animation."""
    console.print("\n🎉 [bold green]Finalizing setup...[/bold green]\n")
    
    with Progress(
        SpinnerColumn(), BarColumn(), TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("Almost Done...", total=3)
        for _ in range(3):
            time.sleep(0.5)
            progress.advance(task)

    console.print("\n")


# 🎯 Main Execution
def main():
    """Initializes the project with an enhanced visual experience."""
    show_welcome_message()

    with Progress(
        SpinnerColumn(), BarColumn(), TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("[cyan]Applying configurations...", total=2)

        # Remove Unnecessary Files
        remove_unnecessary_files()
        progress.advance(task)

        # Copy .env File
        copy_env_file()
        progress.advance(task)

    # 🎉 Final Animation
    celebration_animation()

    console.print(f"\n{SUCCESS} [bold green]Project successfully initialized![/bold green] 🎉")
    show_next_steps()


if __name__ == "__main__":
    main()
