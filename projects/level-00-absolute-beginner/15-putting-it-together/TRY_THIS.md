# Try This — Exercise 15

1. Add a feature that lets the user add a new student. Ask for name and score, then reprint the report.

2. Create your own data file with different students and scores. Make the script read from your file instead.

3. Add a feature that prints only students who scored below 80 (students who need extra help):
   ```python
   print("\nStudents below 80:")
   for student in students:
       if student["score"] < 80:
           print(f"  {student['name']}: {student['score']}")
   ```

4. If you are feeling ambitious: save the report to a new file instead of just printing it. Hint:
   ```python
   with open("report.txt", "w") as f:
       f.write("Student Report\n")
       f.write("Name, Score, Grade\n")
       for student in students:
           grade = get_letter_grade(student["score"])
           f.write(f"{student['name']}, {student['score']}, {grade}\n")
   ```
