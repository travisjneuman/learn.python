# Try This — Project 09

1. Add type validation to `validate_settings()`. Right now it only checks whether required keys exist. Extend it to also check that values have the expected type. Define a schema like this and validate against it:
   ```python
   EXPECTED_TYPES = {
       "port": int,
       "debug": bool,
       "app_name": str,
       "timeout_seconds": int,
   }
   ```
   If `port` is set to `"eight thousand"` instead of `8080`, the validator should catch it.

2. Add a `--set` flag that lets the user override a single setting from the command line, like `--set port=9090`. Parse the key and value from the string, convert the value to the right type (int, bool, or str), and merge it on top of the file settings. Print which setting was overridden:
   ```text
   Override: port = 9090 (was 8080)
   ```

3. Add a `--export` flag that writes the final merged settings to a different format. Support both JSON and a simple `.env` format:
   ```text
   # .env format
   APP_NAME=LearnPython
   DEBUG=true
   PORT=8080
   ```
   Hint: loop through the merged dict, uppercase the key, and convert the value to a string. Write each line as `KEY=value`.

---

| [← Prev](../08-path-exists-checker/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../10-ticket-priority-router/TRY_THIS.md) |
|:---|:---:|---:|
