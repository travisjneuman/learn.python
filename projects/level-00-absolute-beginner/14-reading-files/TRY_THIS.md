# Try This — Exercise 14

1. Create your own data file called `data/my_data.txt` with names and ages (one per line, comma-separated). Modify the exercise to read and print your file instead.

2. Write a script that counts how many lines are in a file:
   ```python
   lines = open("data/sample.txt").readlines()
   print(f"This file has {len(lines)} lines")
   ```

3. Write a script that finds the student with the highest score from the sample data. Hint: keep track of the best name and best score as you loop through lines.
