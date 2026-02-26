# Design Notes — Task Automation System

Fill these out BEFORE you start coding.

## Rule Format

What does a rule look like in your configuration file? Design the schema.

```json
{
    "rules": [
        {
            "name": "...",
            "match": {},
            "action": {},
            "priority": 1
        }
    ]
}
```

What matching criteria will you support? (extension, prefix, size, age, etc.)

## Architecture

Draw the system as components. How do they interact?

```
File Watcher  -->  Rule Engine  -->  Action Executor  -->  Logger
                       |
                  Config Loader
```

What is the flow when a new file appears?

## Safety

What happens if:

- A transform fails halfway through:
- Two rules match the same file:
- The target directory for a move does not exist:
- The system crashes while processing a file:
- A plugin has a bug and raises an exception:

How will you ensure files are never lost or corrupted?

```
(your answer here)
```

## Plugin Architecture (if attempting stretch goal)

How will plugins be discovered and loaded? What interface must a plugin implement?

```python
# What does a plugin look like?
(your answer here)
```

## Module Organization

```
(sketch your file structure here)
```

## Testing Strategy

How will you test file operations without polluting the real filesystem?

```
(your answer here)
```

## Retrospective (fill out AFTER completing the project)

- What went well:
- What was harder than expected:
- What you would do differently:
- What you learned:
