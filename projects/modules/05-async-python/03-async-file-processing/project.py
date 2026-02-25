"""
Async File Processing — Reading and processing files concurrently.

This project shows how to use aiofiles for non-blocking file I/O,
async generators for streaming data, and gather() to process
multiple files at the same time.

Key concepts:
- aiofiles: async versions of open(), read(), write()
- async generators: use "async def" + "yield" to produce values lazily
- async for: iterate over an async generator
"""

import asyncio
import os
import random
import time

import aiofiles


# ── Configuration ────────────────────────────────────────────────────

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
NUM_FILES = 10
LINES_PER_FILE = 50

# Some sample words to generate fake content.
WORDS = [
    "python", "async", "await", "coroutine", "event", "loop", "task",
    "gather", "file", "read", "write", "process", "data", "line",
    "word", "count", "total", "summary", "output", "input",
]


# ── Generate sample files ────────────────────────────────────────────

def generate_sample_files():
    """Create sample text files for processing."""
    os.makedirs(DATA_DIR, exist_ok=True)

    print("--- Generating sample files ---")
    for i in range(1, NUM_FILES + 1):
        filepath = os.path.join(DATA_DIR, f"file_{i:02d}.txt")
        with open(filepath, "w") as f:
            for _ in range(LINES_PER_FILE):
                # Random line of 3-8 words.
                num_words = random.randint(3, 8)
                line = " ".join(random.choices(WORDS, k=num_words))
                f.write(line + "\n")

    print(f"Created {NUM_FILES} sample files in data/\n")


# ── Sync file processing ─────────────────────────────────────────────

def process_file_sync(filepath):
    """Read a file and count lines and words (synchronous)."""
    with open(filepath, "r") as f:
        content = f.read()

    lines = content.strip().split("\n")
    words = sum(len(line.split()) for line in lines)
    filename = os.path.basename(filepath)
    print(f"  Processed {filename}: {len(lines)} lines, {words} words")
    return {"file": filename, "lines": len(lines), "words": words}


def run_sync():
    print("--- Sync file processing ---")
    start = time.time()
    results = []

    for i in range(1, NUM_FILES + 1):
        filepath = os.path.join(DATA_DIR, f"file_{i:02d}.txt")
        results.append(process_file_sync(filepath))

    elapsed = time.time() - start
    total_words = sum(r["words"] for r in results)
    print(f"Sync total: {elapsed:.3f} seconds, {total_words} words across {len(results)} files\n")


# ── Async file processing ────────────────────────────────────────────

async def process_file_async(filepath):
    """Read a file and count lines and words (asynchronous)."""
    # aiofiles.open() returns an async context manager.
    # The actual I/O happens in a thread pool so it doesn't block the event loop.
    async with aiofiles.open(filepath, "r") as f:
        content = await f.read()

    lines = content.strip().split("\n")
    words = sum(len(line.split()) for line in lines)
    filename = os.path.basename(filepath)
    print(f"  Processed {filename}: {len(lines)} lines, {words} words")
    return {"file": filename, "lines": len(lines), "words": words}


async def run_async():
    print("--- Async file processing ---")
    start = time.time()

    # Build a list of coroutines, one per file.
    tasks = []
    for i in range(1, NUM_FILES + 1):
        filepath = os.path.join(DATA_DIR, f"file_{i:02d}.txt")
        tasks.append(process_file_async(filepath))

    # gather() runs all file reads concurrently.
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    total_words = sum(r["words"] for r in results)
    print(f"Async total: {elapsed:.3f} seconds, {total_words} words across {len(results)} files\n")


# ── Async generator demo ─────────────────────────────────────────────
#
# An async generator is like a regular generator but uses "async def"
# and "yield". You iterate it with "async for".

async def read_lines_async(filepath):
    """Yield lines from a file one at a time, asynchronously."""
    async with aiofiles.open(filepath, "r") as f:
        line_num = 0
        # aiofiles supports async iteration over lines.
        async for line in f:
            line_num += 1
            yield line_num, line.strip()


async def demo_async_generator():
    print("--- Async generator demo ---")
    filepath = os.path.join(DATA_DIR, "file_01.txt")

    # "async for" iterates over the async generator.
    # Each iteration may involve an await (reading the next chunk from disk).
    async for line_num, text in read_lines_async(filepath):
        if line_num <= 5:  # Only show first 5 lines.
            print(f"  Yielded line {line_num}: {text}")
        else:
            break

    print(f"  ... (stopped after 5 lines)\n")


# ── Main ─────────────────────────────────────────────────────────────

async def main():
    generate_sample_files()
    run_sync()
    await run_async()
    await demo_async_generator()


if __name__ == "__main__":
    asyncio.run(main())
