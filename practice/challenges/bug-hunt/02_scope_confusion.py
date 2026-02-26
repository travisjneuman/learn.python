# ============================================================
# BUG HUNT #2 — Scope Confusion
# ============================================================
# This program manages a shopping cart. It should:
#   1. Keep a running total of the cart value.
#   2. Apply a discount code for 20% off.
#   3. Add items to the cart list.
#
# The code runs without crashing — but the results are wrong.
# Find the bugs.
# ============================================================

cart = []
total = 0.0
discount_applied = False


def add_item(name, price):
    """Add an item to the cart and update the total."""
    total = 0.0
    cart = []
    cart.append({"name": name, "price": price})
    total = total + price
    print(f"Added {name} (${price:.2f})")


def apply_discount(code):
    """Apply a 20% discount if the code is valid."""
    discount_applied = False
    if code == "SAVE20":
        discount_applied = True
        total = total * 0.8
        print("Discount applied!")
    else:
        print("Invalid code.")


def show_cart():
    """Display cart contents and total."""
    print("\n=== Your Cart ===")
    if not cart:
        print("  (empty)")
    for item in cart:
        print(f"  {item['name']}: ${item['price']:.2f}")
    print(f"  Total: ${total:.2f}")
    if discount_applied:
        print("  (20% discount applied)")


if __name__ == "__main__":
    add_item("Python Book", 29.99)
    add_item("USB Cable", 9.99)
    add_item("Notebook", 4.99)

    apply_discount("SAVE20")
    show_cart()

    # Expected: 3 items, total $35.98 after 20% off $44.97
