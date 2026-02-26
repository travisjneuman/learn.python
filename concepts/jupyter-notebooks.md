# Jupyter Notebooks

Jupyter notebooks let you mix code, text, and visualizations in a single document. They're the standard tool for data exploration, prototyping, and sharing analysis — widely used in data science, machine learning, and scientific computing.

---

## Why Jupyter Matters

When you're exploring data or testing ideas, you don't want to write a full script, run it, tweak it, and run it again. Notebooks let you run code in small chunks (cells) and see the output immediately — including charts, tables, and images. This interactive workflow is why data scientists live in Jupyter.

---

## Installing Jupyter

```bash
# JupyterLab (recommended — modern interface)
pip install jupyterlab
jupyter lab

# Classic Notebook (simpler, still widely used)
pip install notebook
jupyter notebook
```

Both open in your browser at `http://localhost:8888`.

---

## Notebook Basics

A notebook (`.ipynb` file) is a sequence of **cells**. Each cell is either:

### Code Cells

```python
# This runs Python and shows output below the cell
import pandas as pd

df = pd.read_csv("data.csv")
df.head()  # Output appears directly below
```

Press `Shift+Enter` to run a cell and move to the next one.

### Markdown Cells

Write formatted text using Markdown:

```markdown
# Section Title
This is a **bold** explanation with a [link](https://docs.python.org).

- Bullet points work
- So do numbered lists
```

Use markdown cells to document your analysis as you go.

---

## Magic Commands

Jupyter has special commands prefixed with `%` (line) or `%%` (cell):

```python
# Time how long a line takes
%timeit sorted(range(1000))

# Time an entire cell
%%timeit
data = list(range(10000))
sorted(data)

# Run a shell command
!pip install requests

# Show matplotlib plots inline
%matplotlib inline

# List all variables in the namespace
%whos
```

---

## Common Workflow

```python
# Cell 1: Imports
import pandas as pd
import matplotlib.pyplot as plt

# Cell 2: Load data
df = pd.read_csv("sales.csv")

# Cell 3: Explore
df.describe()

# Cell 4: Visualize
df.plot(x="month", y="revenue", kind="bar")
plt.title("Monthly Revenue")
plt.show()

# Cell 5: Analysis
top_month = df.loc[df["revenue"].idxmax()]
print(f"Best month: {top_month['month']} (${top_month['revenue']:,.0f})")
```

Each cell builds on the previous ones. You can go back and re-run any cell.

---

## Exporting Notebooks

```bash
# To Python script
jupyter nbconvert --to script analysis.ipynb

# To HTML (for sharing)
jupyter nbconvert --to html analysis.ipynb

# To PDF (requires pandoc + LaTeX)
jupyter nbconvert --to pdf analysis.ipynb
```

---

## Notebooks vs Scripts

| Use Notebooks When... | Use Scripts When... |
|---|---|
| Exploring data interactively | Building reusable tools |
| Prototyping and experimenting | Running in production |
| Creating shareable analysis | Writing library code |
| Teaching or presenting | Working in CI/CD pipelines |
| Quick visualizations | Code that others import |

**Rule of thumb:** Start in a notebook, then extract reusable code into `.py` files.

---

## Common Mistakes

**Running cells out of order.** Notebooks execute cells in whatever order you click them. If you define `x = 5` in cell 3 but run cell 5 first, `x` won't exist. Always use "Restart & Run All" before sharing.

**Hidden state.** You might delete a cell that defined a variable, but the variable still exists in memory. "Restart & Run All" catches this.

**Notebooks in version control.** `.ipynb` files are JSON with embedded output (images, data). They create messy git diffs. Solutions:
- Clear output before committing
- Use `nbstripout` to auto-strip output on commit
- Use `jupytext` to keep notebooks as `.py` files

---

## JupyterLite — Browser-Based

[JupyterLite](https://jupyter.org/try-jupyter/lab/) runs entirely in your browser — no installation needed. It uses Pyodide (Python compiled to WebAssembly). Great for:
- Quick experiments without setup
- Sharing interactive examples
- Teaching in environments where installing software is difficult

---

## Practice This

- Open JupyterLite and run `import this` (The Zen of Python)
- Create a notebook that loads a CSV and makes a chart
- Try the Module 07 data analysis projects in a notebook
- Export a notebook to HTML and open it in a browser

## Further Reading

- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [Jupyter Notebook Docs](https://jupyter-notebook.readthedocs.io/)
- [Real Python: Jupyter Notebook Introduction](https://realpython.com/jupyter-notebook-introduction/)
- [nbstripout](https://github.com/kynan/nbstripout) — Strip output from notebooks for clean git diffs
