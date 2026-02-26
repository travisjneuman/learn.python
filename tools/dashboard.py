"""
Progress Dashboard — Terminal Learning Dashboard

Displays a rich terminal dashboard showing your learning progress:
XP status, milestone progress, coding streak, and level completion.

Usage:
    python tools/dashboard.py

Requires: rich (pip install rich)
"""

import json
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.columns import Columns
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


def load_json(path):
    """Load a JSON file, returning empty dict if not found."""
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def count_level_projects(level_dir):
    """Count total and completed projects in a level directory."""
    total = 0
    completed = 0
    if not level_dir.exists():
        return total, completed
    for proj in sorted(level_dir.iterdir()):
        if proj.is_dir() and not proj.name.startswith("."):
            total += 1
            # A project is "completed" if it has a project.py with content
            project_file = proj / "project.py"
            if project_file.exists() and project_file.stat().st_size > 100:
                completed += 1
    return total, completed


def run_dashboard_rich():
    """Display the dashboard using the rich library."""
    console = Console()

    # Load data
    xp_config = load_json(REPO_ROOT / "data" / "xp_config.json")
    xp_progress = load_json(REPO_ROOT / "data" / "xp_progress.json")
    streak_data = load_json(REPO_ROOT / "data" / "streak.json")

    total_xp = xp_progress.get("total_xp", 0)
    milestones = xp_config.get("milestones", [])

    # Current and next milestone
    current_ms = None
    next_ms = None
    for ms in milestones:
        if total_xp >= ms["xp"]:
            current_ms = ms
        elif next_ms is None:
            next_ms = ms

    # Header
    title = Text("LEARN.PYTHON DASHBOARD", style="bold cyan")
    console.print(Panel(title, style="cyan"))

    # XP Panel
    ms_name = f"{current_ms['emoji']} {current_ms['name']}" if current_ms else "None"
    xp_text = Text()
    xp_text.append(f"  Total XP: ", style="bold")
    xp_text.append(f"{total_xp:,}\n", style="bold green")
    xp_text.append(f"  Milestone: ", style="bold")
    xp_text.append(f"{ms_name}\n")

    if next_ms:
        remaining = next_ms["xp"] - total_xp
        pct = min(total_xp / next_ms["xp"] * 100, 100)
        xp_text.append(f"  Next: {next_ms['emoji']} {next_ms['name']} ")
        xp_text.append(f"({remaining:,} XP to go, {pct:.0f}%)\n")

    # Streak Panel
    current_streak = streak_data.get("current_streak", 0)
    longest_streak = streak_data.get("longest_streak", 0)
    last_active = streak_data.get("last_active_date", "never")

    # Check if streak is lapsed
    if last_active and last_active != "never":
        diff = (date.today() - date.fromisoformat(last_active)).days
        if diff > 1:
            current_streak = 0

    streak_text = Text()
    streak_text.append(f"  Current: ", style="bold")
    streak_style = "bold green" if current_streak >= 3 else "bold yellow" if current_streak >= 1 else "bold red"
    streak_text.append(f"{current_streak} day(s)\n", style=streak_style)
    streak_text.append(f"  Longest: ", style="bold")
    streak_text.append(f"{longest_streak} day(s)\n")
    streak_text.append(f"  Last active: {last_active}\n")

    # Show side by side
    panels = [
        Panel(xp_text, title="XP Progress", style="green", width=40),
        Panel(streak_text, title="Coding Streak", style="yellow", width=40),
    ]
    console.print(Columns(panels))

    # Level completion table
    table = Table(title="Level Completion", style="cyan")
    table.add_column("Level", style="bold")
    table.add_column("Projects", justify="center")
    table.add_column("Progress", justify="left", width=20)

    projects_dir = REPO_ROOT / "projects"
    for level_num in range(11):
        if level_num == 0:
            level_dir = projects_dir / "level-0"
        else:
            level_dir = projects_dir / f"level-{level_num}"

        if not level_dir.exists():
            continue

        total, completed = count_level_projects(level_dir)
        if total == 0:
            continue

        pct = completed / total * 100
        bar_len = 15
        filled = int(bar_len * pct / 100)
        bar = "#" * filled + "-" * (bar_len - filled)

        if pct >= 80:
            style = "green"
        elif pct >= 40:
            style = "yellow"
        else:
            style = "white"

        table.add_row(
            f"Level {level_num}",
            f"{completed}/{total}",
            f"[{style}][{bar}] {pct:.0f}%[/{style}]",
        )

    # Elite and modules
    elite_dir = projects_dir / "elite-track"
    if elite_dir.exists():
        total, completed = count_level_projects(elite_dir)
        if total > 0:
            pct = completed / total * 100
            filled = int(15 * pct / 100)
            bar = "#" * filled + "-" * (15 - filled)
            table.add_row("Elite", f"{completed}/{total}", f"[{bar}] {pct:.0f}%")

    console.print(table)

    # Recent XP history
    history = list(reversed(xp_progress.get("history", [])))[:5]
    if history:
        console.print()
        hist_table = Table(title="Recent Activity", style="cyan")
        hist_table.add_column("Time", style="dim")
        hist_table.add_column("Activity")
        hist_table.add_column("XP", justify="right", style="green")
        hist_table.add_column("Details")

        for entry in history:
            ts = entry["timestamp"][:16].replace("T", " ")
            activity = entry["activity_type"].replace("_", " ")
            xp = f"+{entry['xp_earned']}"
            details = entry.get("details", "")
            hist_table.add_row(ts, activity, xp, details)

        console.print(hist_table)

    # Next milestone progress bar
    if next_ms:
        console.print()
        prev_xp = current_ms["xp"] if current_ms else 0
        with Progress(
            TextColumn(f"  [bold]Next milestone: {next_ms['emoji']} {next_ms['name']}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("milestone", total=next_ms["xp"] - prev_xp)
            progress.update(task, completed=total_xp - prev_xp)

    console.print()


def run_dashboard_plain():
    """Fallback dashboard without rich — plain ANSI output."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    xp_progress = load_json(REPO_ROOT / "data" / "xp_progress.json")
    xp_config = load_json(REPO_ROOT / "data" / "xp_config.json")
    streak_data = load_json(REPO_ROOT / "data" / "streak.json")

    total_xp = xp_progress.get("total_xp", 0)
    milestones = xp_config.get("milestones", [])

    current_ms = None
    next_ms = None
    for ms in milestones:
        if total_xp >= ms["xp"]:
            current_ms = ms
        elif next_ms is None:
            next_ms = ms

    current_streak = streak_data.get("current_streak", 0)
    longest_streak = streak_data.get("longest_streak", 0)

    print(f"\n{'='*50}")
    print(f"  {BOLD}{CYAN}LEARN.PYTHON DASHBOARD{RESET}")
    print(f"{'='*50}")
    print()
    print(f"  Total XP: {GREEN}{total_xp:,}{RESET}")
    ms_name = f"{current_ms['emoji']} {current_ms['name']}" if current_ms else "None"
    print(f"  Milestone: {ms_name}")
    print(f"  Streak: {YELLOW}{current_streak} day(s){RESET} (longest: {longest_streak})")

    if next_ms:
        remaining = next_ms["xp"] - total_xp
        pct = min(total_xp / next_ms["xp"] * 100, 100)
        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "#" * filled + "-" * (bar_len - filled)
        print(f"  Next: {next_ms['emoji']} {next_ms['name']} [{bar}] {pct:.0f}% ({remaining:,} XP to go)")

    print()


def main():
    if HAS_RICH:
        run_dashboard_rich()
    else:
        print("Note: Install 'rich' for a better dashboard: pip install rich")
        print("Falling back to plain text output.\n")
        run_dashboard_plain()


if __name__ == "__main__":
    main()
