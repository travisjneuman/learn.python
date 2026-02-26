# Solution: Scope Confusion

## Bug 1 — `add_item` creates local variables instead of modifying globals

**Lines:** `total = 0.0` and `cart = []` inside `add_item`

**Problem:** Assigning to `total` and `cart` inside the function creates new
local variables that shadow the module-level ones. The global `cart` and
`total` are never updated.

**Fix:** Declare them as global, or better yet, restructure to avoid globals.
Simplest fix:

```python
def add_item(name, price):
    global cart, total
    cart.append({"name": name, "price": price})
    total = total + price
```

## Bug 2 — `apply_discount` reads `total` before assignment

**Lines:** `discount_applied = False` and `total = total * 0.8`

**Problem:** `discount_applied = False` creates a local variable.
`total = total * 0.8` tries to read the global `total` but Python sees the
assignment and treats `total` as local, causing an `UnboundLocalError`.

**Fix:**

```python
def apply_discount(code):
    global total, discount_applied
    if code == "SAVE20":
        discount_applied = True
        total = total * 0.8
```

## Bug 3 — `show_cart` reads globals but could also fail

The `show_cart` function reads `cart`, `total`, and `discount_applied`. It
works by accident because it never assigns to them. But if `add_item` and
`apply_discount` are not fixed, `show_cart` will show an empty cart and $0.00
total — correct Python, wrong results.
