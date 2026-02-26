# Diagram Index

Visual diagrams for every concept in the curriculum. Diagrams use Mermaid syntax, which renders automatically on GitHub and in the mkdocs documentation site.

Each diagram page includes: an overview map, step-by-step execution flow, decision guides for choosing between related patterns, and comparison diagrams.

---

## Beginner Concepts

| Concept | Diagram Page | Diagram Types |
|---------|-------------|---------------|
| Variables | [Diagrams](../concepts/diagrams/what-is-a-variable.md) | Memory model, type conversion flow |
| Loops | [Diagrams](../concepts/diagrams/how-loops-work.md) | For/while flowcharts, loop selection decision tree |
| Types & Conversions | [Diagrams](../concepts/diagrams/types-and-conversions.md) | Type hierarchy, conversion paths |
| Functions | [Diagrams](../concepts/diagrams/functions-explained.md) | Call stack, parameter flow |
| Collections | [Diagrams](../concepts/diagrams/collections-explained.md) | Collection comparison, selection decision tree |
| Files & Paths | [Diagrams](../concepts/diagrams/files-and-paths.md) | File I/O flow, path resolution |
| Errors & Debugging | [Diagrams](../concepts/diagrams/errors-and-debugging.md) | Exception hierarchy, try/except flow |
| Reading Error Messages | [Diagrams](../concepts/diagrams/reading-error-messages.md) | Traceback anatomy, error type decision tree |

## Intermediate Concepts

| Concept | Diagram Page | Diagram Types |
|---------|-------------|---------------|
| Imports | [Diagrams](../concepts/diagrams/how-imports-work.md) | Import resolution flowchart, sys.path search order |
| Classes & Objects | [Diagrams](../concepts/diagrams/classes-and-objects.md) | Instantiation sequence, inheritance hierarchy, MRO |
| Decorators | [Diagrams](../concepts/diagrams/decorators-explained.md) | Call chain flowchart, stacking order, wrapping |
| Virtual Environments | [Diagrams](../concepts/diagrams/virtual-environments.md) | Creation lifecycle, package isolation |
| Comprehensions | [Diagrams](../concepts/diagrams/comprehensions-explained.md) | Data flow pipeline, comprehension vs loop |
| Args & Kwargs | [Diagrams](../concepts/diagrams/args-kwargs-explained.md) | Argument matching flow, unpacking |
| Context Managers | [Diagrams](../concepts/diagrams/context-managers-explained.md) | Enter/exit lifecycle, with statement flow |
| Enums | [Diagrams](../concepts/diagrams/enums-explained.md) | Value mapping, flag composition |
| Type Hints | [Diagrams](../concepts/diagrams/type-hints-explained.md) | Type annotation hierarchy, generics flow |
| Dataclasses | [Diagrams](../concepts/diagrams/dataclasses-explained.md) | Auto-generation flow, frozen vs mutable |

## Advanced Concepts

| Concept | Diagram Page | Diagram Types |
|---------|-------------|---------------|
| HTTP | [Diagrams](../concepts/diagrams/http-explained.md) | Request/response sequence, status codes |
| APIs | [Diagrams](../concepts/diagrams/api-basics.md) | REST architecture, CRUD mapping, auth flow |
| Async/Await | [Diagrams](../concepts/diagrams/async-explained.md) | Event loop state machine, task lifecycle |
| Testing Strategies | [Diagrams](../concepts/diagrams/testing-strategies.md) | Testing pyramid, TDD cycle |
| Generators & Iterators | [Diagrams](../concepts/diagrams/generators-and-iterators.md) | Iterator protocol, yield flow |
| Collections Deep Dive | [Diagrams](../concepts/diagrams/collections-deep-dive.md) | Collection decision tree, performance |
| Functools & Itertools | [Diagrams](../concepts/diagrams/functools-and-itertools.md) | Decorator chain, lru_cache flow |
| Terminal Deeper | [Diagrams](../concepts/diagrams/the-terminal-deeper.md) | Shell pipeline, I/O flow |
| Regex | [Diagrams](../concepts/diagrams/regex-explained.md) | Matching flow, pattern decision tree |
| Security Basics | [Diagrams](../concepts/diagrams/security-basics.md) | OWASP overview, sanitization flow |

## Module Architecture

| Module | Diagram Page | Diagram Types |
|--------|-------------|---------------|
| FastAPI | [Diagrams](../concepts/diagrams/fastapi-request-lifecycle.md) | Request lifecycle, dependency injection flow |
| Django | [Diagrams](../concepts/diagrams/django-mtv-pattern.md) | MTV pattern, URL routing, ORM flow |
| Docker | [Diagrams](../concepts/diagrams/docker-architecture.md) | Container lifecycle, compose services, networking |
| Async Event Loop | [Diagrams](../concepts/diagrams/async-event-loop.md) | Event loop states, task scheduling, gather vs wait |
| SQLAlchemy ORM | [Diagrams](../concepts/diagrams/sqlalchemy-orm-mapping.md) | Engine/Session/Model mapping, query execution |
| Web Scraping | [Diagrams](../concepts/diagrams/web-scraping-pipeline.md) | Fetch/parse/extract pipeline, rate limiting |
| CI/CD | [Diagrams](../concepts/diagrams/ci-cd-pipeline.md) | Push/lint/test/build/deploy stages |
| Cloud Deployment | [Diagrams](../concepts/diagrams/cloud-deployment-topology.md) | Local/staging/production topology |

---

## How to Read Mermaid Diagrams

Mermaid diagrams render automatically on GitHub. If you are viewing these files locally in a text editor, you will see the raw Mermaid syntax. To render them:

1. **GitHub:** Just open the file — diagrams render automatically
2. **VS Code:** Install the "Mermaid Markdown Syntax Highlighting" extension
3. **mkdocs site:** Visit the [documentation site](https://travisjneuman.github.io/learn.python)
4. **Mermaid Live Editor:** Paste the code at [mermaid.live](https://mermaid.live)

---

| [Home](../README.md) |
|:---:|
