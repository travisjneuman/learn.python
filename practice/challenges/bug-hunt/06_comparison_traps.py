# ============================================================
# BUG HUNT #6 — Comparison Traps
# ============================================================
# This program validates and processes form input. It should:
#   1. Check if a value is empty or missing.
#   2. Compare prices for equality.
#   3. Categorize items by truthiness.
#   4. Validate age ranges.
#
# Python comparison operators have gotchas. Find them.
# ============================================================


def is_empty(value):
    """Return True if the value is None, empty string, or empty list."""
    if value is "":
        return True
    if value is []:
        return True
    if value is None:
        return True
    return False


def prices_match(price_a, price_b):
    """Check if two calculated prices are the same."""
    # Simulating prices from different calculations
    return price_a == price_b


def categorize_values(values):
    """Split values into 'truthy' and 'falsy' groups."""
    truthy = []
    falsy = []
    for v in values:
        if v == True:
            truthy.append(v)
        elif v == False:
            falsy.append(v)
    return truthy, falsy


def validate_age(age):
    """Check that age is between 0 and 150 inclusive."""
    if age is not None and 0 < age < 150:
        return True
    return False


if __name__ == "__main__":
    # Test is_empty
    print("=== Empty Checks ===")
    print(f'is_empty(""): {is_empty("")}')       # Should be True
    print(f"is_empty([]): {is_empty([])}")         # Should be True
    print(f"is_empty(None): {is_empty(None)}")     # Should be True
    print(f"is_empty(0): {is_empty(0)}")           # Should be False (0 is not "empty")

    # Test price comparison
    print("\n=== Price Match ===")
    a = 0.1 + 0.2
    b = 0.3
    print(f"0.1 + 0.2 == 0.3? {prices_match(a, b)}")  # Should be True

    # Test categorize
    print("\n=== Categorize ===")
    test_values = [1, 0, "", "hello", None, True, False, [], [1, 2]]
    truthy, falsy = categorize_values(test_values)
    print(f"Truthy: {truthy}")   # Should be [1, "hello", True, [1, 2]]
    print(f"Falsy: {falsy}")     # Should be [0, "", None, False, []]

    # Test age validation
    print("\n=== Age Validation ===")
    print(f"Age 0 valid? {validate_age(0)}")     # Should be True (newborn)
    print(f"Age 150 valid? {validate_age(150)}") # Should be True (boundary)
    print(f"Age 25 valid? {validate_age(25)}")   # Should be True
    print(f"Age -1 valid? {validate_age(-1)}")   # Should be False
