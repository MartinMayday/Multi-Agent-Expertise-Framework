import typer
from pathlib import Path
from src.memory.context_manager import ContextManager

app = typer.Typer(help="Expert Framework Memory Operations")

@app.command()
def init():
    """Initialize .context structure in current directory."""
    cm = ContextManager()
    paths = [
        "00_rules",
        "01_state",
        "02_memory",
        "03_archive/sessions"
    ]
    for p in paths:
        path = cm.get_project_path(p)
        path.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created {path}")
    
    # Create initial files
    project_md = cm.get_project_path("00_rules/project.md")
    if not project_md.exists():
        project_md.write_text("# Project Constitution\n\nDefine mission and architecture here.")

@app.command()
def status():
    """Show memory status."""
    cm = ContextManager()
    session_path = cm.get_project_path("01_state/active_session.json")
    if session_path.exists():
        session = cm.load_json(session_path)
        typer.echo(f"Active Session: {session.get('id')}")
        typer.echo(f"Goal: {session.get('goal')}")
    else:
        typer.echo("No active session.")

if __name__ == "__main__":
    app()
