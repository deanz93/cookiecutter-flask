import subprocess
import sys
from rich.console import Console

console = Console()

# ✅ Check & Install Dependencies
def ensure_dependencies():
    """Automatically install missing dependencies."""
    required_packages = ["rich", "alive-progress"]
    
    for package in required_packages:
        try:
            __import__(package)  # Try importing the package
        except ImportError:
            console.print(f"⚠️  [yellow]Dependency '{package}' not found. Installing now...[/yellow]")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            console.print(f"✅ [green]Successfully installed {package}![/green]\n")

ensure_dependencies()  # Run the check before everything else
