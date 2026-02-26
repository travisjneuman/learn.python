# Capstone 01 — Personal Finance Tracker

## Brief

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

Build a CLI personal finance tracker that helps a user understand where their money goes.

## Requirements

### Core (must have)

- **Add transactions:** Record income and expenses with a date, amount, description, and category.
- **Categorize spending:** Assign categories (food, rent, transport, entertainment, etc.) to each transaction. Support custom categories.
- **Monthly summaries:** Show total income, total spending, net savings, and a breakdown by category for any given month.
- **CSV import/export:** Import transactions from a CSV file. Export all transactions to CSV.
- **Persistent storage:** Transactions must survive between program runs. Choose your storage format (JSON, CSV, SQLite, etc.).

### Stretch (pick at least one)

- **Budget alerts:** Set a monthly budget per category. Warn the user when spending exceeds 80% or 100% of the budget.
- **Recurring transactions:** Support monthly recurring items (e.g., rent, salary) that auto-generate entries.
- **Year-over-year comparison:** Show how spending in a category this month compares to the same month last year.
- **Data visualization:** Generate a simple bar chart or table of spending by category (use matplotlib or just ASCII art).

## Constraints

- Python 3.11+ with standard library. External packages only if a stretch goal requires them.
- Must have a clear CLI interface (use `input()` prompts, `argparse`, or `click`/`typer`).
- Must include tests for the core logic (not the CLI input/output layer).

## Deliverables

- Working application code
- Tests (`python -m pytest tests/`)
- Filled-out `notes.md` with your design decisions
- A `README.md` in your project explaining how to install and run it

## Architecture decisions are yours

There is no starter code. You decide:
- How to organize your files and modules
- How to store data
- How to structure the CLI
- How to handle errors
- What to test and how

Fill out `notes.md` before you start coding.
