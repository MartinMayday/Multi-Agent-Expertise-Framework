import typer
from src.cli import memory

app = typer.Typer(help="Multi-Agent Expertise Framework CLI")
app.add_typer(memory.app, name="memory")

@app.command()
def version():
    """Show framework version."""
    typer.echo("Expert Framework v0.1.0")

def main():
    app()

if __name__ == "__main__":
    main()
