# Try This — Project 07

1. Add a `countdown` command that tells you how many days are left until a given date. If the date is in the past, it should say how many days ago it was:
   ```text
   countdown 2026-12-31  =>  307 days from now
   countdown 2024-01-01  =>  788 days ago
   ```
   Hint: compare the target date with `datetime.now()` and check whether the difference is positive or negative.

2. Add a `range` command that lists every date between two dates, one per line, along with the day of the week:
   ```text
   range 2026-03-01 2026-03-05
     2026-03-01  Sunday
     2026-03-02  Monday
     2026-03-03  Tuesday
     2026-03-04  Wednesday
     2026-03-05  Thursday
   ```
   Hint: use a `while` loop with `timedelta(days=1)` to step through each day.

3. Add a `workdays` command that counts only Monday-through-Friday days between two dates (skipping weekends). Compare the result to `days_between()` so the user can see how many weekend days fall in the range:
   ```text
   workdays 2026-03-01 2026-03-15  =>  10 workdays (4 weekend days skipped)
   ```
   Hint: use `.weekday()` which returns 0 for Monday through 6 for Sunday.

---

| [← Prev](../06-simple-gradebook-engine/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../08-path-exists-checker/TRY_THIS.md) |
|:---|:---:|---:|
