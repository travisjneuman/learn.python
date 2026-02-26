# Web Scraping Pipeline — Diagrams

[<- Back to Diagram Index](../../guides/DIAGRAM_INDEX.md)

## Overview

These diagrams trace the full web scraping workflow from fetching a page to storing structured data, including politeness strategies, error handling, and the parse-extract-transform pipeline.

## End-to-End Scraping Pipeline

A well-structured scraper separates fetching, parsing, extraction, transformation, and storage into distinct stages. Each stage has a clear responsibility and failure mode.

```mermaid
flowchart TD
    URL["Target URL<br/>https://example.com/products"] --> FETCH["Fetch<br/>requests.get(url, headers, timeout)"]
    FETCH --> CHECK{"Status OK?"}
    CHECK -->|"200"| PARSE["Parse HTML<br/>BeautifulSoup(html, 'html.parser')"]
    CHECK -->|"403/429"| RETRY["Rate Limited or Blocked<br/>Wait, rotate headers, retry"]
    CHECK -->|"404/500"| LOG["Log Error<br/>Skip URL, continue"]
    RETRY --> FETCH

    PARSE --> EXTRACT["Extract Data<br/>soup.select('div.product')<br/>CSS selectors or find_all()"]
    EXTRACT --> TRANSFORM["Transform & Clean<br/>Strip whitespace<br/>Convert price to float<br/>Normalize dates"]
    TRANSFORM --> VALIDATE{"Data valid?"}
    VALIDATE -->|"Yes"| STORE["Store<br/>CSV, JSON, SQLite, or API"]
    VALIDATE -->|"No"| DISCARD["Log & Discard<br/>Missing required fields"]

    STORE --> NEXT{"More pages?"}
    NEXT -->|"Yes"| DELAY["Polite Delay<br/>time.sleep(1-3)"]
    DELAY --> URL
    NEXT -->|"No"| DONE["Done<br/>Report: N items scraped"]

    style FETCH fill:#4a9eff,stroke:#2670c2,color:#fff
    style PARSE fill:#cc5de8,stroke:#9c36b5,color:#fff
    style EXTRACT fill:#ff922b,stroke:#e8590c,color:#fff
    style TRANSFORM fill:#ffd43b,stroke:#f59f00,color:#000
    style STORE fill:#51cf66,stroke:#27ae60,color:#fff
    style RETRY fill:#ff6b6b,stroke:#c92a2a,color:#fff
```

**Key points:**
- Always set a `timeout` on requests to avoid hanging forever on unresponsive servers
- Separate extraction (finding elements) from transformation (cleaning data) for clearer code
- Validate extracted data before storing: catch missing fields early
- Add delays between requests to avoid overwhelming the target server

## Politeness and Rate Limiting Strategy

Responsible scraping means respecting the server. These strategies prevent your scraper from being blocked and keep you on the right side of server policies.

```mermaid
flowchart TD
    START["Before Scraping"] --> ROBOTS["Check robots.txt<br/>Respect Disallow rules"]
    ROBOTS --> HEADERS["Set Realistic Headers<br/>User-Agent, Accept, Accept-Language"]
    HEADERS --> STRATEGY{"Choose Strategy"}

    STRATEGY --> FIXED["Fixed Delay<br/>time.sleep(2)<br/>Simple, predictable"]
    STRATEGY --> RANDOM["Random Delay<br/>time.sleep(random.uniform(1, 3))<br/>Looks more natural"]
    STRATEGY --> ADAPTIVE["Adaptive Delay<br/>Slow down on 429s<br/>Speed up on 200s"]

    subgraph ANTI_BLOCK ["Anti-Blocking Techniques"]
        ROTATE_UA["Rotate User-Agents<br/>Random browser string per request"]
        SESSION_USE["Use requests.Session()<br/>Maintain cookies naturally"]
        CACHE["Cache Responses<br/>Don't re-fetch unchanged pages"]
    end

    FIXED --> ANTI_BLOCK
    RANDOM --> ANTI_BLOCK
    ADAPTIVE --> ANTI_BLOCK

    subgraph LIMITS ["Know Your Limits"]
        RESPECT["Respect rate limit headers<br/>X-RateLimit-Remaining<br/>Retry-After"]
        TOS["Check Terms of Service<br/>Some sites prohibit scraping"]
        API_FIRST["Prefer APIs when available<br/>Structured data, no parsing needed"]
    end

    style START fill:#51cf66,stroke:#27ae60,color:#fff
    style ANTI_BLOCK fill:#ffd43b,stroke:#f59f00,color:#000
    style LIMITS fill:#ff922b,stroke:#e8590c,color:#fff
```

**Key points:**
- Always check `robots.txt` before scraping (it tells you which paths are off-limits)
- Random delays between 1-3 seconds look more natural than fixed intervals
- Rotate User-Agent strings to reduce the chance of being fingerprinted
- If the site has a public API, use it instead of scraping HTML

## Parse and Extract: BeautifulSoup Workflow

The parsing stage turns raw HTML into a navigable tree. Understanding selector strategies helps you write resilient scrapers that survive minor page layout changes.

```mermaid
flowchart TD
    HTML["Raw HTML String<br/>response.text"] --> SOUP["BeautifulSoup(html, 'html.parser')<br/>Builds parse tree"]

    SOUP --> SELECT_STRATEGY{"Selector Strategy"}

    SELECT_STRATEGY --> CSS["CSS Selectors<br/>soup.select('div.product &gt; h2 a')<br/>Familiar, powerful"]
    SELECT_STRATEGY --> FIND["find / find_all<br/>soup.find_all('a', class_='product-link')<br/>Pythonic, flexible"]
    SELECT_STRATEGY --> XPATH_ALT["Tag Navigation<br/>tag.parent / tag.next_sibling<br/>For tricky layouts"]

    CSS --> DATA["Extract Data"]
    FIND --> DATA
    XPATH_ALT --> DATA

    DATA --> TEXT["element.get_text(strip=True)<br/>Clean text content"]
    DATA --> ATTR["element['href']<br/>element.get('src', '')<br/>Attribute values"]
    DATA --> NESTED["element.select_one('.price')<br/>Nested element search"]

    TEXT --> DICT["Build dict per item<br/>{'name': ..., 'price': ..., 'url': ...}"]
    ATTR --> DICT
    NESTED --> DICT

    DICT --> LIST["Collect all items<br/>items.append(dict)"]

    style SOUP fill:#cc5de8,stroke:#9c36b5,color:#fff
    style CSS fill:#4a9eff,stroke:#2670c2,color:#fff
    style FIND fill:#4a9eff,stroke:#2670c2,color:#fff
    style DATA fill:#ffd43b,stroke:#f59f00,color:#000
    style DICT fill:#51cf66,stroke:#27ae60,color:#fff
```

**Key points:**
- CSS selectors (`select`) are usually the cleanest approach for well-structured HTML
- `get_text(strip=True)` removes whitespace; `get('attr', default)` safely accesses attributes
- Build a dictionary per item, then collect into a list for easy CSV/JSON export
- Test selectors interactively in a Python shell before writing the full scraper

---

| [Back to Diagram Index](../../guides/DIAGRAM_INDEX.md) |
|:---:|
