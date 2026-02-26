# Design Notes — API Aggregator

Fill these out BEFORE you start coding.

## API Selection

Which APIs will you use? Why these ones?

| API | URL | What data it provides | Auth required? |
|-----|-----|----------------------|----------------|
| 1. | | | |
| 2. | | | |
| 3. (optional) | | | |

## Common Schema

Each API returns different JSON. What does your normalized format look like?

```json
{
    "source": "...",
    "timestamp": "...",
    "type": "...",
    "data": {}
}
```

What fields are common across all sources? What fields are source-specific?

## Caching Strategy

How will you cache responses? Where are they stored? How long before they expire?

```
(your answer here)
```

What happens when the cache file is corrupted or missing?

## Error Handling

What happens when:

- API returns a 500 error:
- API returns unexpected JSON shape:
- Network is completely down:
- One API is slow (10+ second response):
- Rate limit exceeded (429 response):

## Module Organization

```
(sketch your file structure here)
```

## Testing Strategy

How will you test code that makes HTTP requests? What will you mock?

```
(your answer here)
```

## Retrospective (fill out AFTER completing the project)

- What went well:
- What was harder than expected:
- What you would do differently:
- What you learned:
