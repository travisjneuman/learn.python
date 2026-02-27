"""
Progress Dashboard — Terminal Learning Dashboard

Displays a terminal dashboard showing your learning progress:
XP status, coding streak, level completion (parsed from PROGRESS.md),
and module progress — all in one view.

Usage:
    python tools/dashboard.py              # full dashboard
    python tools/dashboard.py --plain      # force plain ASCII (no rich)

Requires: rich (pip install rich) for the enhanced view.
Falls back to plain ASCII if rich is not installed.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROGRESS_MD = REPO_ROOT / "PROGRESS.md"

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.columns import Columns
    from rich.text import Text

    HAS_RICH = True
except ImportError:
    HAS_RICH = False


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    """Load a JSON file, returning empty dict if missing."""
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def parse_progress_md() -> dict[str, tuple[int, int]]:
    """Parse PROGRESS.md and count checked / total boxes per section.

    Returns a dict mapping section key -> (completed, total).
    Section keys follow patterns like:
        "Level 00", "Level 0", ..., "Level 10",
        "Elite Track", "Capstone Projects",
        "Module 01", ..., "Module 12",
        "Gate A", "Gate B", etc.
    """
    if not PROGRESS_MD.exists():
        return {}

    with open(PROGRESS_MD, encoding="utf-8") as f:
        text = f.read()

    sections: dict[str, tuple[int, int]] = {}
    current_key: str | None = None

    # Patterns for section headers we care about
    level_re = re.compile(
        r"^##\s+Level\s+(\d+)\b", re.IGNORECASE
    )
    level_00_re = re.compile(
        r"^##\s+Level\s+00\b", re.IGNORECASE
    )
    gate_re = re.compile(
        r"^##\s+(Gate\s+\w+)", re.IGNORECASE
    )
    elite_re = re.compile(
        r"^###?\s+Elite\s+Track", re.IGNORECASE
    )
    capstone_re = re.compile(
        r"^##\s+Capstone\s+Projects", re.IGNORECASE
    )
    module_re = re.compile(
        r"^###\s+Module\s+(\d+)", re.IGNORECASE
    )
    # Generic section header (## or ###) — used to reset current_key
    header_re = re.compile(r"^#{2,3}\s+")

    checked_re = re.compile(r"^-\s*\[x\]", re.IGNORECASE)
    unchecked_re = re.compile(r"^-\s*\[\s\]")

    for line in text.splitlines():
        stripped = line.strip()

        # Try to match a section header
        m_level00 = level_00_re.match(stripped)
        m_level = level_re.match(stripped)
        m_gate = gate_re.match(stripped)
        m_elite = elite_re.match(stripped)
        m_capstone = capstone_re.match(stripped)
        m_module = module_re.match(stripped)

        if m_level00:
            current_key = "Level 00"
        elif m_level:
            num = int(m_level.group(1))
            current_key = f"Level {num}"
        elif m_gate:
            current_key = m_gate.group(1)
        elif m_elite:
            current_key = "Elite Track"
        elif m_capstone:
            current_key = "Capstone Projects"
        elif m_module:
            num = int(m_module.group(1))
            current_key = f"Module {num:02d}"
        elif header_re.match(stripped):
            # Some other section we don't track — keep current_key only
            # if it's a subsection (###) under a tracked section; otherwise
            # reset to avoid counting stray checkboxes.
            if not stripped.startswith("###"):
                current_key = None
            continue

        if current_key is None:
            continue

        # Count checkboxes
        if checked_re.match(stripped):
            done, total = sections.get(current_key, (0, 0))
            sections[current_key] = (done + 1, total + 1)
        elif unchecked_re.match(stripped):
            done, total = sections.get(current_key, (0, 0))
            sections[current_key] = (done, total + 1)

    return sections


def count_filesystem_projects(level_dir: Path) -> int:
    """Count project subdirectories in a level directory."""
    if not level_dir.exists():
        return 0
    return sum(
        1 for p in level_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


# ---------------------------------------------------------------------------
# Build the unified progress data
# ---------------------------------------------------------------------------

# Expected project counts per section (from filesystem).
# These serve as fallback totals when PROGRESS.md doesn't list
# individual items for a section.
LEVEL_DIRS = {
    "Level 00": "level-00-absolute-beginner",
    "Level 0": "level-0",
    "Level 1": "level-1",
    "Level 2": "level-2",
    "Level 3": "level-3",
    "Level 4": "level-4",
    "Level 5": "level-5",
    "Level 6": "level-6",
    "Level 7": "level-7",
    "Level 8": "level-8",
    "Level 9": "level-9",
    "Level 10": "level-10",
}

MODULE_DIRS = {
    "Module 01": "01-web-scraping",
    "Module 02": "02-cli-tools",
    "Module 03": "03-rest-apis",
    "Module 04": "04-fastapi-web",
    "Module 05": "05-async-python",
    "Module 06": "06-databases-orm",
    "Module 07": "07-data-analysis",
    "Module 08": "08-testing-advanced",
    "Module 09": "09-docker-deployment",
    "Module 10": "10-django-fullstack",
    "Module 11": "11-package-publishing",
    "Module 12": "12-cloud-deploy",
}

def _detect_encoding() -> str:
    """Return the effective output encoding for the current terminal."""
    return sys.stdout.encoding or "utf-8"


def safe_str(text: str) -> str:
    """Return text with unencodable characters replaced by '?' for the
    current terminal encoding. Prevents UnicodeEncodeError on Windows
    terminals that use cp1252 or similar limited encodings."""
    encoding = _detect_encoding()
    return text.encode(encoding, errors="replace").decode(encoding)


def safe_emoji(emoji: str) -> str:
    """Return the emoji if the terminal can render it, otherwise '*'."""
    encoding = _detect_encoding()
    try:
        emoji.encode(encoding)
        return emoji
    except (UnicodeEncodeError, UnicodeDecodeError):
        return "*"


MODULE_NAMES = {
    "Module 01": "Web Scraping",
    "Module 02": "CLI Tools",
    "Module 03": "REST APIs",
    "Module 04": "FastAPI",
    "Module 05": "Async Python",
    "Module 06": "Databases & ORM",
    "Module 07": "Data Analysis",
    "Module 08": "Adv. Testing",
    "Module 09": "Docker & Deploy",
    "Module 10": "Django Full-Stack",
    "Module 11": "Pkg Publishing",
    "Module 12": "Cloud Deploy",
}

LEVEL_NAMES = {
    "Level 00": "Absolute Beginner",
    "Level 0": "Terminal & Basic I/O",
    "Level 1": "Functions & Modular Code",
    "Level 2": "Collections",
    "Level 3": "File Automation",
    "Level 4": "JSON & Structured Data",
    "Level 5": "Exception Handling",
    "Level 6": "SQL Basics",
    "Level 7": "ETL Pipelines",
    "Level 8": "APIs & Async",
    "Level 9": "Advanced Patterns",
    "Level 10": "Systems Integration",
}


def build_section_data(
    section_key: str,
    md_sections: dict[str, tuple[int, int]],
    fs_dir: Path | None = None,
) -> tuple[int, int]:
    """Return (completed, total) for a section.

    Prefers PROGRESS.md counts. If the section has no checkboxes there,
    falls back to filesystem project count with 0 completed.
    """
    if section_key in md_sections:
        return md_sections[section_key]
    if fs_dir and fs_dir.exists():
        total = count_filesystem_projects(fs_dir)
        return (0, total)
    return (0, 0)


# ---------------------------------------------------------------------------
# ASCII progress bar (plain, no rich dependency)
# ---------------------------------------------------------------------------

def ascii_bar(done: int, total: int, width: int = 20) -> str:
    """Return a bracketed ASCII bar like [========            ] 5/15."""
    if total == 0:
        return f"[{'':>{width}}]  0/0"
    pct = done / total
    filled = int(width * pct)
    bar = "=" * filled + " " * (width - filled)
    return f"[{bar}] {done:>3}/{total}"


# ---------------------------------------------------------------------------
# Rich dashboard
# ---------------------------------------------------------------------------

def run_dashboard_rich(console: Console) -> None:
    """Display the full dashboard using the rich library."""
    md_sections = parse_progress_md()

    # Load gamification data
    xp_config = load_json(REPO_ROOT / "data" / "xp_config.json")
    xp_progress = load_json(REPO_ROOT / "data" / "xp_progress.json")
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

    # Streak
    current_streak = streak_data.get("current_streak", 0)
    longest_streak = streak_data.get("longest_streak", 0)
    last_active = streak_data.get("last_active_date", "never")
    if last_active and last_active != "never":
        diff = (date.today() - date.fromisoformat(last_active)).days
        if diff > 1:
            current_streak = 0

    # ---- Header ----
    console.print()
    console.print(
        Panel(
            Text("LEARN.PYTHON PROGRESS DASHBOARD", style="bold cyan", justify="center"),
            style="cyan",
        )
    )

    # ---- XP + Streak side-by-side ----
    ms_name = (
        f"{safe_emoji(current_ms['emoji'])} {current_ms['name']}" if current_ms else "None yet"
    )
    xp_text = Text()
    xp_text.append("  Total XP: ", style="bold")
    xp_text.append(f"{total_xp:,}\n", style="bold green")
    xp_text.append("  Milestone: ", style="bold")
    xp_text.append(f"{ms_name}\n")
    if next_ms:
        remaining = next_ms["xp"] - total_xp
        pct = min(total_xp / next_ms["xp"] * 100, 100) if next_ms["xp"] else 0
        xp_text.append(
            f"  Next: {safe_emoji(next_ms['emoji'])} {next_ms['name']} "
            f"({remaining:,} XP to go, {pct:.0f}%)\n"
        )

    streak_text = Text()
    streak_text.append("  Current: ", style="bold")
    s_style = (
        "bold green" if current_streak >= 3
        else "bold yellow" if current_streak >= 1
        else "bold red"
    )
    streak_text.append(f"{current_streak} day(s)\n", style=s_style)
    streak_text.append("  Longest: ", style="bold")
    streak_text.append(f"{longest_streak} day(s)\n")
    streak_text.append(f"  Last active: {last_active}\n")

    panels = [
        Panel(xp_text, title="XP Progress", style="green", width=42),
        Panel(streak_text, title="Coding Streak", style="yellow", width=42),
    ]
    console.print(Columns(panels))

    # ---- Level completion table ----
    table = Table(title="Level Completion", style="cyan", show_lines=False)
    table.add_column("Level", style="bold", min_width=8)
    table.add_column("Name", min_width=22)
    table.add_column("Done", justify="right", width=6)
    table.add_column("Progress", min_width=26)

    projects_dir = REPO_ROOT / "projects"
    grand_done = 0
    grand_total = 0

    for key in [f"Level {n}" for n in ["00"] + list(range(11))]:
        dir_name = LEVEL_DIRS.get(key, "")
        fs_dir = projects_dir / dir_name if dir_name else None
        done, total = build_section_data(key, md_sections, fs_dir)
        grand_done += done
        grand_total += total

        pct = (done / total * 100) if total else 0
        bar_w = 20
        filled = int(bar_w * pct / 100)
        bar_str = "=" * filled + " " * (bar_w - filled)

        if pct >= 100:
            color = "bold green"
        elif pct >= 50:
            color = "yellow"
        else:
            color = "white"

        name = LEVEL_NAMES.get(key, "")
        table.add_row(
            key,
            name,
            f"{done}/{total}",
            f"[{color}][{bar_str}] {pct:>3.0f}%[/{color}]",
        )

    # Elite Track
    done, total = build_section_data(
        "Elite Track", md_sections, projects_dir / "elite-track"
    )
    grand_done += done
    grand_total += total
    pct = (done / total * 100) if total else 0
    filled = int(20 * pct / 100)
    bar_str = "=" * filled + " " * (20 - filled)
    color = "bold green" if pct >= 100 else "yellow" if pct >= 50 else "white"
    table.add_row(
        "Elite",
        "Elite Track",
        f"{done}/{total}",
        f"[{color}][{bar_str}] {pct:>3.0f}%[/{color}]",
    )

    # Capstones
    done, total = build_section_data(
        "Capstone Projects", md_sections, projects_dir / "capstones"
    )
    grand_done += done
    grand_total += total
    pct = (done / total * 100) if total else 0
    filled = int(20 * pct / 100)
    bar_str = "=" * filled + " " * (20 - filled)
    color = "bold green" if pct >= 100 else "yellow" if pct >= 50 else "white"
    table.add_row(
        "Capstone",
        "Capstone Projects",
        f"{done}/{total}",
        f"[{color}][{bar_str}] {pct:>3.0f}%[/{color}]",
    )

    # Grand total row
    g_pct = (grand_done / grand_total * 100) if grand_total else 0
    g_filled = int(20 * g_pct / 100)
    g_bar = "=" * g_filled + " " * (20 - g_filled)
    g_color = "bold green" if g_pct >= 100 else "cyan" if g_pct >= 50 else "white"
    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        "",
        f"[bold]{grand_done}/{grand_total}[/bold]",
        f"[{g_color}][{g_bar}] {g_pct:>3.0f}%[/{g_color}]",
    )

    console.print(table)

    # ---- Modules table ----
    mod_table = Table(title="Expansion Modules", style="magenta", show_lines=False)
    mod_table.add_column("Module", style="bold", min_width=11)
    mod_table.add_column("Name", min_width=18)
    mod_table.add_column("Done", justify="right", width=6)
    mod_table.add_column("Progress", min_width=26)

    mod_grand_done = 0
    mod_grand_total = 0

    for key, dir_name in MODULE_DIRS.items():
        fs_dir = projects_dir / "modules" / dir_name
        done, total = build_section_data(key, md_sections, fs_dir)
        mod_grand_done += done
        mod_grand_total += total

        pct = (done / total * 100) if total else 0
        filled = int(20 * pct / 100)
        bar_str = "=" * filled + " " * (20 - filled)
        color = "bold green" if pct >= 100 else "yellow" if pct >= 50 else "white"
        name = MODULE_NAMES.get(key, "")
        mod_table.add_row(
            key,
            name,
            f"{done}/{total}",
            f"[{color}][{bar_str}] {pct:>3.0f}%[/{color}]",
        )

    m_pct = (mod_grand_done / mod_grand_total * 100) if mod_grand_total else 0
    m_filled = int(20 * m_pct / 100)
    m_bar = "=" * m_filled + " " * (20 - m_filled)
    m_color = (
        "bold green" if m_pct >= 100
        else "cyan" if m_pct >= 50
        else "white"
    )
    mod_table.add_section()
    mod_table.add_row(
        "[bold]TOTAL[/bold]",
        "",
        f"[bold]{mod_grand_done}/{mod_grand_total}[/bold]",
        f"[{m_color}][{m_bar}] {m_pct:>3.0f}%[/{m_color}]",
    )

    console.print(mod_table)

    # ---- Recent XP history ----
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

    # ---- Footer ----
    overall_done = grand_done + mod_grand_done
    overall_total = grand_total + mod_grand_total
    overall_pct = (overall_done / overall_total * 100) if overall_total else 0

    console.print()
    footer = Text()
    footer.append("  Overall: ", style="bold")
    footer.append(f"{overall_done}/{overall_total} projects ", style="bold cyan")
    footer.append(f"({overall_pct:.1f}% complete)", style="dim")
    footer.append("\n  Track progress: edit PROGRESS.md checkboxes ", style="dim")
    footer.append("[ ] -> [x]", style="bold dim")
    console.print(Panel(footer, style="dim"))
    console.print()


# ---------------------------------------------------------------------------
# Plain ASCII dashboard (no rich dependency)
# ---------------------------------------------------------------------------

def run_dashboard_plain() -> None:
    """Fallback dashboard using only print() and basic ANSI codes."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    md_sections = parse_progress_md()
    projects_dir = REPO_ROOT / "projects"

    # Load gamification data
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
    last_active = streak_data.get("last_active_date", "never")
    if last_active and last_active != "never":
        diff = (date.today() - date.fromisoformat(last_active)).days
        if diff > 1:
            current_streak = 0

    # Header
    print()
    print(f"  {BOLD}{CYAN}{'=' * 58}{RESET}")
    print(f"  {BOLD}{CYAN}       LEARN.PYTHON PROGRESS DASHBOARD{RESET}")
    print(f"  {BOLD}{CYAN}{'=' * 58}{RESET}")
    print()

    # XP + Streak
    ms_name = (
        f"{safe_emoji(current_ms['emoji'])} {current_ms['name']}" if current_ms else "None yet"
    )
    print(safe_str(f"  XP: {GREEN}{total_xp:,}{RESET}  |  Milestone: {ms_name}"))
    print(
        f"  Streak: {YELLOW}{current_streak} day(s){RESET}"
        f"  |  Longest: {longest_streak}  |  Last active: {last_active}"
    )
    if next_ms:
        remaining = next_ms["xp"] - total_xp
        pct = min(total_xp / next_ms["xp"] * 100, 100) if next_ms["xp"] else 0
        print(safe_str(
            f"  Next: {safe_emoji(next_ms['emoji'])} {next_ms['name']}"
            f" ({remaining:,} XP to go, {pct:.0f}%)"
        ))
    print()

    # Level completion
    print(f"  {BOLD}LEVEL COMPLETION{RESET}")
    print(f"  {'-' * 58}")

    grand_done = 0
    grand_total = 0
    bar_w = 20

    for key in [f"Level {n}" for n in ["00"] + list(range(11))]:
        dir_name = LEVEL_DIRS.get(key, "")
        fs_dir = projects_dir / dir_name if dir_name else None
        done, total = build_section_data(key, md_sections, fs_dir)
        grand_done += done
        grand_total += total
        name = LEVEL_NAMES.get(key, "")
        label = f"{key:>8}  {name:<24}"
        bar = ascii_bar(done, total, bar_w)
        color = GREEN if done == total and total > 0 else YELLOW if done > 0 else ""
        end = RESET if color else ""
        print(f"  {color}{label}{bar}{end}")

    # Elite
    done, total = build_section_data(
        "Elite Track", md_sections, projects_dir / "elite-track"
    )
    grand_done += done
    grand_total += total
    label = f"{'Elite':>8}  {'Elite Track':<24}"
    bar = ascii_bar(done, total, bar_w)
    color = GREEN if done == total and total > 0 else YELLOW if done > 0 else ""
    end = RESET if color else ""
    print(f"  {color}{label}{bar}{end}")

    # Capstones
    done, total = build_section_data(
        "Capstone Projects", md_sections, projects_dir / "capstones"
    )
    grand_done += done
    grand_total += total
    label = f"{'Capstone':>8}  {'Capstone Projects':<24}"
    bar = ascii_bar(done, total, bar_w)
    color = GREEN if done == total and total > 0 else YELLOW if done > 0 else ""
    end = RESET if color else ""
    print(f"  {color}{label}{bar}{end}")

    print(f"  {'-' * 58}")
    g_pct = (grand_done / grand_total * 100) if grand_total else 0
    g_bar = ascii_bar(grand_done, grand_total, bar_w)
    print(f"  {BOLD}{'TOTAL':>8}  {'':<24}{g_bar}  {g_pct:.0f}%{RESET}")
    print()

    # Module completion
    print(f"  {BOLD}EXPANSION MODULES{RESET}")
    print(f"  {'-' * 58}")

    mod_grand_done = 0
    mod_grand_total = 0

    for key, dir_name in MODULE_DIRS.items():
        fs_dir = projects_dir / "modules" / dir_name
        done, total = build_section_data(key, md_sections, fs_dir)
        mod_grand_done += done
        mod_grand_total += total
        name = MODULE_NAMES.get(key, "")
        label = f"{key:>9}  {name:<22}"
        bar = ascii_bar(done, total, bar_w)
        color = GREEN if done == total and total > 0 else YELLOW if done > 0 else ""
        end = RESET if color else ""
        print(f"  {color}{label}{bar}{end}")

    print(f"  {'-' * 58}")
    m_pct = (mod_grand_done / mod_grand_total * 100) if mod_grand_total else 0
    m_bar = ascii_bar(mod_grand_done, mod_grand_total, bar_w)
    print(f"  {BOLD}{'TOTAL':>9}  {'':<22}{m_bar}  {m_pct:.0f}%{RESET}")
    print()

    # Footer
    overall_done = grand_done + mod_grand_done
    overall_total = grand_total + mod_grand_total
    overall_pct = (overall_done / overall_total * 100) if overall_total else 0
    print(
        f"  {BOLD}Overall: {CYAN}{overall_done}/{overall_total} projects"
        f" ({overall_pct:.1f}% complete){RESET}"
    )
    print(f"  {DIM}Track progress: edit PROGRESS.md checkboxes [ ] -> [x]{RESET}")
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    force_plain = "--plain" in sys.argv

    if HAS_RICH and not force_plain:
        console = Console()
        run_dashboard_rich(console)
    else:
        if not HAS_RICH:
            print("Tip: Install 'rich' for an enhanced dashboard: pip install rich")
            print("Showing plain ASCII output.\n")
        run_dashboard_plain()


if __name__ == "__main__":
    main()
