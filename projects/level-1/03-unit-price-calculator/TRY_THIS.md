# Try This — Project 03

1. Add a "buy recommendation" feature. After ranking the products, print a recommendation like `"Buy 2x Rice 10lb Bag to save $3.00 vs buying Rice 5lb Bag"`. Compare the cost of buying equivalent quantities of the cheapest vs most expensive option.

2. Add support for different units in the same comparison. Right now the program assumes all products use the same unit. What if one row says `"kg"` and another says `"lb"`? Add a `convert_to_kg()` function that converts pounds to kilograms (1 lb = 0.4536 kg) so the unit prices are comparable.

3. Add a `--budget` flag that takes a dollar amount. Filter the output to show only products you could afford, and print how many units of the best deal you could buy with that budget:
   ```text
   Budget: $50.00
   Best deal: Rice 10lb Bag at $1.55/lb
   You could buy: 3 bags ($46.47), $3.53 remaining
   ```

---

| [← Prev](../02-password-strength-checker/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../04-log-line-parser/TRY_THIS.md) |
|:---|:---:|---:|
