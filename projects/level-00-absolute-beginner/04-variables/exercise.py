# ============================================================
# Exercise 04: Variables
# ============================================================
#
# A variable is a name that holds a value.
# Think of it like a labeled box. You put something in the box
# and use the label to get it back later.
#
# The = sign means "store this value in this name".
# It does NOT mean "equals" like in math class.
# It means "put the thing on the right into the name on the left".
# ============================================================

# Create a variable called "name" and store the text "Alice" in it.
name = "Alice"

# Now we can use the variable name instead of typing the text again.
print(name)

# Create more variables.
age = 30
city = "Denver"

# Use variables in print statements.
print("Name:", name)
print("Age:", age)
print("City:", city)

# You can change what a variable holds at any time.
# The old value is gone. The new value replaces it.
age = 31
print("Next year I will be", age)

# You can use variables in math.
hours_per_day = 8
days_per_week = 5
hours_per_week = hours_per_day * days_per_week
print("I work", hours_per_week, "hours per week")

# You can combine text variables (this is called "concatenation").
first_name = "Alice"
last_name = "Neuman"
full_name = first_name + " " + last_name
print("Full name:", full_name)

# ============================================================
# NAMING RULES:
#
# Variable names can contain letters, numbers, and underscores.
# They CANNOT start with a number.
# They are case-sensitive: "Name" and "name" are different variables.
# Use lowercase with underscores for readability: hours_per_week
# ============================================================
