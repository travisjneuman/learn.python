# Try This — Project 06

1. Add a grade distribution summary that counts how many students got each letter grade. Print it as a simple bar chart using `#` characters:
   ```text
   Grade Distribution:
     A: ###        (3 students)
     B: #####      (5 students)
     C: ##         (2 students)
     D:            (0 students)
     F: #          (1 student)
   ```
   Hint: loop through your students and use a dictionary to count each letter grade.

2. Add a `--drop-lowest` flag that drops each student's lowest score before computing their average. For example, if a student scored `[80, 90, 60, 95]`, drop the `60` and average the remaining `[80, 90, 95]`. Use `min()` to find the lowest score, and `list.remove()` to take it out. Be careful: work on a copy of the list so you do not modify the original.

3. Add a "students at risk" report that prints students whose average is within 5 points of a grade boundary (e.g., a student with 88 is close to the A threshold of 90). This helps identify students who might benefit from extra support:
   ```text
   Students near a grade boundary:
     Bob Smith: 88.0 (2 points below A)
     Eve Davis: 59.5 (0.5 points below D)
   ```

---

| [← Prev](../05-csv-first-reader/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../07-date-difference-helper/TRY_THIS.md) |
|:---|:---:|---:|
