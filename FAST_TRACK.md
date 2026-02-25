# Fast Track — Python for Experienced Developers

Home: [README](./README.md)

Already know another programming language? This guide tells you what to skip, what to skim, and where to jump in.

---

## Who This Is For

You should use this guide if you can answer "yes" to all of these:

- You already know at least one programming language well
- You understand variables, loops, functions, and classes conceptually
- You have used a terminal before
- You have used git before

If any of those are "no," start at [START_HERE.md](./START_HERE.md) and follow the normal path. There is no shame in it — the foundations matter.

---

## What to Skip, Skim, and Study

| Document | Action | Why |
|----------|--------|-----|
| 00_COMPUTER_LITERACY_PRIMER | **Skip** | You already know what a terminal is |
| 01_ROADMAP | **Skim** | 5 minutes to understand the curriculum structure |
| 02_GLOSSARY | **Skim** | Scan for Python-specific terms you don't know |
| 03_SETUP_ALL_PLATFORMS | **Do** | You still need Python installed correctly |
| 04_FOUNDATIONS | **Study** | Python syntax differs from other languages in important ways |
| Level 00 exercises | **Skip** | Too basic for you |
| Level 0 projects | **Skim + test** | Do 3–4 projects to learn Python's file I/O and testing conventions |
| Level 1–2 projects | **Select** | Pick 5 projects total that cover unfamiliar ground |
| Level 3+ | **Full curriculum** | This is where Python-specific patterns start mattering |

---

## Python for JavaScript Developers

### Key Differences

| Concept | JavaScript | Python |
|---------|-----------|--------|
| Variables | `let x = 5` / `const x = 5` | `x = 5` (no keyword, all mutable by default) |
| Strings | `'single'`, `"double"`, `` `template` `` | `'single'`, `"double"`, `f"template {var}"` |
| Arrays/Lists | `[1, 2, 3]` — `Array` methods | `[1, 2, 3]` — list methods (different names) |
| Objects/Dicts | `{key: value}` | `{"key": value}` (keys must be quoted) |
| None/null | `null` / `undefined` | `None` (one concept, not two) |
| Truthiness | `0`, `""`, `null`, `undefined`, `NaN` | `0`, `""`, `None`, `[]`, `{}`, `set()` |
| Iteration | `for...of`, `forEach`, `.map()` | `for x in collection:` — list comprehensions |
| Async | `async/await` + Promises | `async/await` + asyncio (event loop is explicit) |
| Imports | `import/require` (ES modules/CJS) | `import` (always — no require) |
| Scope | Function + block (`let`/`const`) | Function scope + `global`/`nonlocal` keywords |
| Classes | `class` with `constructor` | `class` with `__init__` + `self` everywhere |
| Type system | Dynamic (TypeScript for types) | Dynamic (type hints are optional annotations) |
| Package manager | npm / yarn / pnpm | pip / uv |
| Formatting | Prettier | Black / Ruff format |
| Linting | ESLint | Ruff |

### What Will Surprise You

1. **Indentation is syntax.** No braces. Get used to it.
2. **`self` is explicit.** Every method takes `self` as its first argument.
3. **No `this` weirdness.** `self` always means the instance. No binding issues.
4. **List comprehensions replace `.map()` and `.filter()`.** `[x*2 for x in items if x > 0]`
5. **Tuples are immutable lists.** `(1, 2, 3)` — used everywhere for return values.
6. **Slicing is powerful.** `items[1:5]`, `items[::-1]` (reverse), `items[::2]` (every other).
7. **No semicolons.** Ever.

### Start Here

Jump to the [04_FOUNDATIONS.md](./04_FOUNDATIONS.md) doc and skim through it, pausing on anything unfamiliar. Then do Level 0 projects 06, 08, 11, 14, and 15 to get your hands dirty. Move to Level 3 for the real work.

---

## Python for Java Developers

### Key Differences

| Concept | Java | Python |
|---------|------|--------|
| Types | Static, declared | Dynamic, inferred (type hints optional) |
| Entry point | `public static void main(String[] args)` | `if __name__ == "__main__":` |
| Compilation | Compiled to bytecode → JVM | Interpreted (also compiles to bytecode, but transparent) |
| Variables | `int x = 5;` | `x = 5` |
| Strings | Immutable `String`, `StringBuilder` | Immutable `str`, f-strings for formatting |
| Collections | `ArrayList`, `HashMap`, `HashSet` | `list`, `dict`, `set` (built-in, no imports) |
| Null | `null` → NullPointerException | `None` → AttributeError |
| Interfaces | `interface` keyword | Abstract base classes or duck typing |
| Generics | `List<String>` | `list[str]` (type hints, not enforced at runtime) |
| Exceptions | Checked + unchecked | All unchecked (no `throws` clause) |
| File I/O | `BufferedReader`, try-with-resources | `open()`, `with` statement |
| Build tool | Maven / Gradle | pip + pyproject.toml (or uv) |
| Testing | JUnit | pytest |

### What Will Surprise You

1. **No type declarations required.** Python figures it out. Type hints exist but are optional.
2. **Everything is an object.** Integers, functions, classes — everything.
3. **No access modifiers.** No `public`/`private`/`protected`. Convention: prefix with `_` for private.
4. **Duck typing.** If it has a `.read()` method, it is file-like. No interface required.
5. **Multiple return values.** Functions return tuples: `return x, y, z`
6. **Decorators replace annotations.** `@staticmethod`, `@property`, `@dataclass`
7. **No boilerplate.** No getters/setters (use `@property`), no `equals`/`hashCode` (use `@dataclass`).

### Start Here

Read [04_FOUNDATIONS.md](./04_FOUNDATIONS.md) carefully — Python's simplicity will feel strange after Java. Do Level 0 projects 03, 06, 10, 13, and 15 to calibrate. Then jump to Level 3.

---

## Python for C# Developers

### Key Differences

| Concept | C# | Python |
|---------|-----|--------|
| Types | Static, strong | Dynamic, strong |
| LINQ | `.Where()`, `.Select()` | List comprehensions, `filter()`, `map()` |
| Properties | `get; set;` | `@property` decorator |
| Async | `async/await` + `Task` | `async/await` + `asyncio` |
| Dependency injection | Framework-level (DI containers) | Manual or simple factories |
| Namespaces | `namespace X.Y.Z` | Packages (directory + `__init__.py`) |
| NuGet | Package manager | pip / uv |
| .NET Framework | Runtime | CPython interpreter |

### What Will Surprise You

1. **No solution/project files.** Just directories and `.py` files.
2. **No compilation step.** Run directly: `python script.py`
3. **`with` statement replaces `using`.** Same concept for resource management.
4. **Dictionaries are first-class.** Used everywhere — config, kwargs, data.
5. **REPL is your friend.** Type `python` in terminal for an interactive session.

### Start Here

Skim [04_FOUNDATIONS.md](./04_FOUNDATIONS.md), do Level 0 projects 05, 08, 12, and 15, then jump to Level 3.

---

## Python for Ruby Developers

### Key Differences

| Concept | Ruby | Python |
|---------|------|--------|
| Blocks | `do...end`, `{ }` | No blocks — use functions, lambdas, comprehensions |
| Symbols | `:name` | Just use strings |
| Methods | Implicit return | Explicit `return` (or implicit `None`) |
| Truthiness | Only `nil` and `false` are falsy | `0`, `""`, `None`, `[]`, `{}`, `set()` are falsy |
| Iteration | `.each`, `.map`, `.select` | `for` loops, list comprehensions |
| Gems | Bundler + Gemfile | pip + requirements.txt (or uv + pyproject.toml) |
| Rails | Web framework | Django (similar philosophy) or FastAPI |

### What Will Surprise You

1. **Explicit is better than implicit.** Python prefers `self.name` over Ruby's `@name`.
2. **No implicit returns.** You must write `return value`.
3. **Indentation matters.** No `end` keyword — blocks are defined by indentation.
4. **No method_missing.** Python has `__getattr__` but it is used less.
5. **Community prefers readability over cleverness.** "There should be one obvious way to do it."

### Start Here

Skim [04_FOUNDATIONS.md](./04_FOUNDATIONS.md), do 4–5 Level 0 projects to feel the syntax, then jump to Level 3.

---

## Language Comparison Table

Quick reference for common operations:

| Operation | Python | JavaScript | Java | C# | Ruby |
|-----------|--------|-----------|------|-----|------|
| Print | `print(x)` | `console.log(x)` | `System.out.println(x)` | `Console.WriteLine(x)` | `puts x` |
| String format | `f"Hello {name}"` | `` `Hello ${name}` `` | `"Hello " + name` | `$"Hello {name}"` | `"Hello #{name}"` |
| List/Array | `[1, 2, 3]` | `[1, 2, 3]` | `List.of(1, 2, 3)` | `new List<int>{1,2,3}` | `[1, 2, 3]` |
| Dict/Map | `{"a": 1}` | `{a: 1}` | `Map.of("a", 1)` | `new Dictionary<>()` | `{a: 1}` |
| Iterate | `for x in items:` | `for (x of items)` | `for (var x : items)` | `foreach (var x in items)` | `items.each do \|x\|` |
| Lambda | `lambda x: x*2` | `x => x*2` | `x -> x*2` | `x => x*2` | `->(x) { x*2 }` |
| Null check | `if x is None:` | `if (x === null)` | `if (x == null)` | `if (x == null)` | `if x.nil?` |
| Try/Catch | `try/except` | `try/catch` | `try/catch` | `try/catch` | `begin/rescue` |
| Import | `import os` | `import x from 'y'` | `import java.util.*` | `using System;` | `require 'x'` |

---

## Recommended Fast-Track Path

```
Week 1:  Setup (Doc 03) → Foundations (Doc 04) → Level 0 (selected projects)
Week 2:  Level 1 (selected) → Level 2 (selected) → Concept docs for gaps
Week 3:  Level 3 (full) → Module 01 or 03
Week 4:  Level 4 (full) → Module 04 (FastAPI)
Week 5+: Continue normal curriculum from Level 5
```

Estimated time to reach Level 5 competency: 4–6 weeks at 10–15 hours per week. Compare to 12–16 weeks for someone starting from zero.

---

## Concepts That Trip Up Experienced Developers

Even if you know other languages well, these Python-specific topics deserve study:

1. **The GIL** — Python's Global Interpreter Lock means threads do not run in parallel for CPU work. Use `multiprocessing` or `asyncio` instead.
2. **Mutable default arguments** — `def f(items=[])` is a classic bug. The list is shared across calls.
3. **Everything is a reference** — `a = [1,2,3]; b = a; b.append(4)` modifies both.
4. **Comprehensions vs generators** — `[x for x in range(10)]` creates a list; `(x for x in range(10))` creates a lazy generator.
5. **`__init__` vs `__new__`** — You almost always want `__init__`. `__new__` is for metaclass magic.
6. **Context managers** — The `with` statement is Python's RAII. Use it for files, locks, connections.
7. **Decorators** — Not annotations. They wrap functions. Understand closures first.

Read the relevant concept docs in `concepts/` for detailed explanations of each.

---

| [← Career Readiness](./CAREER_READINESS.md) | [Home](./README.md) | [Changelog →](./CHANGELOG.md) |
|:---|:---:|---:|
