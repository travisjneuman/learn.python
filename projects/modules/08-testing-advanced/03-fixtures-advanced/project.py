"""
Project 03 — Fixtures Advanced

A FileProcessor class that reads configuration from environment variables,
processes text files, and writes output. This is the kind of code that
benefits from pytest fixtures because:

1. It reads environment variables (need monkeypatch to test safely)
2. It reads/writes files (need tmp_path for isolated file operations)
3. It has setup steps that many tests share (need conftest.py fixtures)
"""

import os


class FileProcessor:
    """
    A text file processor that is configured via environment variables.

    In a real application, this might process log files, transform CSV data,
    or clean up text before feeding it to another system. The pattern of
    "read config from env vars, process files, write output" is extremely
    common in production Python code.
    """

    def __init__(self):
        # Configuration is loaded on demand, not in __init__.
        # This lets tests set up environment variables before calling load_config.
        self.config = None

    def load_config(self):
        """
        Read configuration from environment variables.

        Environment variables are the standard way to configure applications
        in production (see "12-factor app" methodology). Each variable has
        a default so the app works even without explicit configuration.
        """
        self.config = {
            # APP_MODE controls whether we uppercase, lowercase, or leave
            # the text unchanged. Default is "uppercase".
            "mode": os.environ.get("APP_MODE", "uppercase"),

            # APP_STRIP controls whether we strip leading/trailing whitespace
            # from each line. Default is "true".
            "strip_whitespace": os.environ.get("APP_STRIP", "true").lower() == "true",

            # APP_OUTPUT_DIR is where processed files are saved.
            # Default is "output" (relative to the current directory).
            "output_dir": os.environ.get("APP_OUTPUT_DIR", "output"),
        }
        return self.config

    def process_file(self, file_path):
        """
        Read a text file and process its contents according to the config.

        Returns a list of processed lines.
        Raises FileNotFoundError if the file does not exist.
        """
        # Make sure config is loaded. This is a common defensive pattern:
        # load config on first use if it has not been loaded yet.
        if self.config is None:
            self.load_config()

        # Read the file. We do not catch FileNotFoundError here because
        # the caller should know if the file does not exist.
        with open(file_path, "r") as f:
            lines = f.readlines()

        processed = []
        for line in lines:
            # Step 1: optionally strip whitespace.
            if self.config["strip_whitespace"]:
                line = line.strip()
            else:
                # Even if we are not stripping, remove the trailing newline.
                # readlines() includes the \n at the end of each line.
                line = line.rstrip("\n")

            # Step 2: apply the text transformation mode.
            if self.config["mode"] == "uppercase":
                line = line.upper()
            elif self.config["mode"] == "lowercase":
                line = line.lower()
            # If mode is anything else, leave the line unchanged.

            processed.append(line)

        return processed

    def save_results(self, lines, output_path):
        """
        Write processed lines to an output file.

        Creates parent directories if they do not exist.
        Each line is written followed by a newline character.
        """
        # Create the directory if it does not exist. os.makedirs with
        # exist_ok=True is safe to call even if the directory already exists.
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Write each line followed by a newline.
        with open(output_path, "w") as f:
            for line in lines:
                f.write(line + "\n")

        return output_path


# ── Demo ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("FileProcessor Demo")
    print("=" * 40)
    print()

    # Create a sample input file for the demo.
    sample_input = "demo_input.txt"
    with open(sample_input, "w") as f:
        f.write("  Hello World  \n")
        f.write("  this is a test  \n")
        f.write("  Python is great  \n")

    # Create and configure the processor.
    processor = FileProcessor()
    config = processor.load_config()
    print(f"Config: {config}")
    print()

    # Process the file.
    results = processor.process_file(sample_input)
    print("Processed lines:")
    for line in results:
        print(f"  '{line}'")
    print()

    # Save results.
    output_path = processor.save_results(results, "demo_output.txt")
    print(f"Results saved to: {output_path}")

    # Clean up demo files.
    os.remove(sample_input)
    os.remove(output_path)
    print("Demo files cleaned up.")
