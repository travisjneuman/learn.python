# Try This — Exercise 12

1. Create a dictionary for your favorite movie with keys: title, year, director, rating. Print each value.

2. Build a simple word counter:
   ```python
   words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
   counts = {}
   for word in words:
       if word in counts:
           counts[word] = counts[word] + 1
       else:
           counts[word] = 1
   print(counts)
   ```

3. Try accessing a key that does not exist (like `person["salary"]`). Read the error. Then try using `.get()` which returns None instead of crashing:
   ```python
   print(person.get("salary"))          # None
   print(person.get("salary", "N/A"))   # "N/A" (default value)
   ```
