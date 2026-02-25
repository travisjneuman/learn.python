# Try This — Exercise 08

1. Build an age checker that uses `input()`:
   ```python
   age = int(input("Enter your age: "))
   if age >= 18:
       print("You are an adult.")
   else:
       print("You are a minor.")
   ```

2. Build a number guesser:
   ```python
   secret = 7
   guess = int(input("Guess a number 1-10: "))
   if guess == secret:
       print("Correct!")
   elif guess < secret:
       print("Too low!")
   else:
       print("Too high!")
   ```

3. Change the `temperature` and `score` values in the exercise file. Run it again. Predict what the output will be BEFORE running it. Were you right?

---

| [← Prev](../07-user-input/TRY_THIS.md) | [Home](../../../README.md) | [Next →](../09-lists/TRY_THIS.md) |
|:---|:---:|---:|
