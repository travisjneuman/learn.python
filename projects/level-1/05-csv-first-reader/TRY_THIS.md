# Try This — Project 05

1. Add a `--sort` flag that sorts the table by a given column name. For example, `--sort salary` should display rows ordered by salary (highest first for numeric columns, alphabetical for text columns). Hint: use `sorted()` with a `key` function that checks whether the column is numeric.

2. Add a row-filtering feature with `--where`. For example, `--where "salary>70000"` should only show rows where the salary is greater than 70000. Start simple: split the filter string on `>` or `<` to get the column name, operator, and value.
   ```python
   # Example parsing:
   column, value = filter_str.split(">")
   # Then compare: float(row[column]) > float(value)
   ```

3. Add a `--export` flag that writes the table to a new CSV file. But here is the twist: only include the columns the user selected with `--columns` (if provided), and only include the rows that passed the `--where` filter (if provided). This combines your earlier extensions into one workflow.

---

| [← Prev](../04-log-line-parser/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../06-simple-gradebook-engine/TRY_THIS.md) |
|:---|:---:|---:|
