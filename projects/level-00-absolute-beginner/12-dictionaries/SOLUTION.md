# Solution: 12-dictionaries

> **STOP** — Have you attempted this project yourself first?
>
> Learning happens in the struggle, not in reading answers.
> Spend at least 20 minutes trying before reading this solution.
> If you are stuck, try first — it guides
> your thinking without giving away the answer.

---


## Complete solution

```python
# Create a dictionary
person = {
    "name": "Alice",      # WHY: Each line is a key-value pair — "name" is the key (the label), "Alice" is the value (the data)
    "age": 30,            # WHY: Keys are always strings (in quotes), values can be any type — here it is a number
    "city": "Denver",     # WHY: The curly braces {} and colons : are what make this a dictionary, not a list
    "job": "Engineer"     # WHY: Trailing comma after the last item is optional but considered good style — it makes adding new lines easier
}

# Access a value by its key
print("Name:", person["name"])    # WHY: Use square brackets with the KEY name to get the VALUE — like looking up a word in a real dictionary
print("Age:", person["age"])      # WHY: You ask for "age" and get back 30 — the key is the question, the value is the answer

# Print the whole dictionary
print("Full person:", person)     # WHY: Printing a dictionary shows all key-value pairs — useful for debugging to see everything at once

# Add a new key-value pair
person["hobby"] = "coding"        # WHY: Assigning to a key that does not exist yet CREATES it — the dictionary grows dynamically
print("After adding hobby:", person)  # WHY: The dictionary now has 5 pairs instead of 4

# Change an existing value
person["age"] = 31                # WHY: Assigning to a key that already exists REPLACES the old value — 30 is gone, 31 takes its place
print("After birthday:", person)

# Remove a key-value pair
del person["job"]                 # WHY: "del" (delete) removes the key AND its value — the dictionary shrinks by one pair
print("After removing job:", person)

# Check if a key exists
if "name" in person:              # WHY: "in" checks if a KEY exists in the dictionary — it does NOT search the values
    print("Name is in the dictionary.")

if "salary" not in person:        # WHY: "not in" checks for absence — important to check before accessing a key that might not exist
    print("Salary is NOT in the dictionary.")

# Loop through a dictionary
print()
print("All info about this person:")
for key, value in person.items():  # WHY: .items() gives you BOTH the key and value on each loop — you get two variables instead of one
    print(f"  {key}: {value}")     # WHY: Prints each pair on its own line — "name: Alice", "age: 31", etc.

# A more practical example — a phone book
phone_book = {
    "Alice": "555-0101",          # WHY: The person's name is the key, their phone number is the value — you look up the name to find the number
    "Bob": "555-0102",
    "Charlie": "555-0103"
}

name = "Bob"                      # WHY: Store the name to look up — in a real program this would come from user input
print(f"\n{name}'s number is {phone_book[name]}")  # WHY: phone_book["Bob"] returns "555-0102" — instant lookup by name, no loop needed
```

## Design decisions

| Decision | Why | Alternative considered |
|----------|-----|----------------------|
| Use string keys with descriptive names | Keys like "name", "age", "city" make the data self-documenting — you know exactly what each value represents | Could use numeric keys (like a list), but then you lose the ability to look up data by label |
| Show `del` for removing pairs | `del` is the simplest way to remove a key-value pair — one word, one operation | `.pop("job")` also removes a key and returns its value, which is useful if you need the value. But `del` is simpler for beginners |
| Demonstrate the phone book pattern | Looking up a number by name is exactly what dictionaries are designed for — it connects the abstract concept to something familiar | Could use another example, but everyone understands phone books |
| Use `.items()` for looping | `.items()` gives you both key and value, which is what you almost always want when looping through a dictionary | `.keys()` gives just keys, `.values()` gives just values — but `.items()` is the most versatile |

## Alternative approaches

### Approach B: A word counter (from TRY_THIS.md)

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]  # WHY: A list with repeated words — we want to count how many times each appears
counts = {}                                                         # WHY: Start with an empty dictionary — we will build it up word by word

for word in words:                    # WHY: Look at each word in the list, one at a time
    if word in counts:                # WHY: Check if we have seen this word before — if the key exists, we have counted it at least once
        counts[word] = counts[word] + 1  # WHY: Add 1 to the existing count — "apple" was 1, now it is 2
    else:
        counts[word] = 1             # WHY: First time seeing this word — create the key and start the count at 1

print(counts)                        # WHY: Prints {'apple': 3, 'banana': 2, 'cherry': 1} — a frequency count of every word
```

**Trade-off:** This "count occurrences" pattern is one of the most common uses for dictionaries in real programming. It appears in data analysis, text processing, inventory tracking, and log analysis. The if/else check for whether the key exists is the standard pattern, though Python has shortcuts (`.get()` and `collections.Counter`) that you will learn later.

### Approach C: Using `.get()` for safe lookups

```python
person = {"name": "Alice", "age": 30}

# Dangerous: crashes if the key does not exist
# print(person["salary"])  # KeyError!

# Safe: .get() returns None (or a default) if the key is missing
salary = person.get("salary")             # WHY: Returns None instead of crashing — None means "no value"
print(f"Salary: {salary}")                # WHY: Prints "Salary: None" — you can check for None to know the key was missing

salary = person.get("salary", "N/A")     # WHY: The second argument is a default value — used when the key does not exist
print(f"Salary: {salary}")                # WHY: Prints "Salary: N/A" — much friendlier than a crash

name = person.get("name", "Unknown")     # WHY: If the key DOES exist, .get() returns the real value — the default is ignored
print(f"Name: {name}")                    # WHY: Prints "Name: Alice" — the default "Unknown" is not used because "name" exists
```

**Trade-off:** `.get()` is safer than square brackets because it never crashes. Use `person["name"]` when you are SURE the key exists. Use `person.get("name")` when the key MIGHT be missing. In professional code, `.get()` is extremely common.

## What could go wrong

| Scenario | What happens | Prevention |
|----------|-------------|------------|
| Accessing a key that does not exist: `person["salary"]` | `KeyError: 'salary'` — Python crashes because there is no key called "salary" | Check first with `if "salary" in person:` or use `.get("salary")` which returns None instead of crashing |
| Using a list as a key: `{[1,2]: "value"}` | `TypeError: unhashable type: 'list'` — lists cannot be dictionary keys | Keys must be immutable types: strings, numbers, or tuples. Strings are by far the most common |
| Confusing dictionaries and lists | Trying `person[0]` thinking it returns the first item — dictionaries have no order concept in that sense | Lists use numeric indices (`[0]`, `[1]`). Dictionaries use named keys (`["name"]`, `["age"]`). They are different tools |
| Modifying a dictionary while looping through it | `RuntimeError: dictionary changed size during iteration` — Python stops the program | Loop through a copy: `for key in list(person.keys()):` — or build a separate list of changes |
| Forgetting quotes around keys: `person[name]` instead of `person["name"]` | Python looks for a VARIABLE called `name` — if it does not exist, you get a `NameError`. If it does exist, you get whatever value `name` holds | Use quotes for literal key names: `person["name"]`. Without quotes, Python thinks you mean a variable |

## Key takeaways

1. **Dictionaries store labeled data as key-value pairs** — they are the perfect tool when your data has names or labels, not just positions. A person's name, age, and city naturally fit a dictionary. A list of scores naturally fits a list. Choosing the right container makes your code clearer and faster.
2. **Lookup by key is instant** — `person["name"]` finds "Alice" immediately, even in a dictionary with millions of entries. Lists have to search one by one to find a value. This speed difference is why dictionaries are used for phone books, caches, configurations, and any lookup table.
3. **Dictionaries are everywhere in real Python** — JSON data from web APIs, configuration files, database results, and function arguments all use dictionaries. The pattern of creating, reading, updating, and deleting key-value pairs (often called CRUD) is the foundation of data management in every programming language.
