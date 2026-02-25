# ============================================================
# Exercise 08: Making Decisions (if / else)
# ============================================================
#
# Programs need to make decisions. "If this is true, do that.
# Otherwise, do something else."
#
# Python uses if, elif (else if), and else for this.
#
# INDENTATION MATTERS. The indented lines after if/elif/else
# are the code that runs when that condition is true.
# Use 4 spaces for each indent level.
# ============================================================

# Simple if/else
temperature = 75

if temperature > 80:
    print("It is hot outside.")
else:
    print("It is not too hot.")

# if / elif / else — multiple conditions
score = 85

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")

# Comparison operators:
#   ==   equal to (TWO equals signs, not one!)
#   !=   not equal to
#   >    greater than
#   <    less than
#   >=   greater than or equal to
#   <=   less than or equal to

# Checking equality
password = "secret123"

if password == "secret123":
    print("Access granted.")
else:
    print("Access denied.")

# Combining conditions with "and" / "or"
age = 25
has_license = True

if age >= 16 and has_license:
    print("You can drive.")
else:
    print("You cannot drive.")

# "not" flips a condition
is_raining = False

if not is_raining:
    print("No umbrella needed.")

# ============================================================
# COMMON MISTAKE:
#
# Using = (assignment) instead of == (comparison):
#   if x = 5:    # WRONG — this stores 5 in x
#   if x == 5:   # RIGHT — this checks if x equals 5
# ============================================================
