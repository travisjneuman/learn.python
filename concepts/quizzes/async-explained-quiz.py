"""
Quiz: Async Explained
Review: concepts/async-explained.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Async Explained")
    print("  Review: concepts/async-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What problem does async solve?")
    print()
    print("  a) Makes CPU-heavy math faster")
    print("  b) Lets your program do useful work while waiting for")
    print("     slow operations like network requests")
    print("  c) Reduces memory usage")
    print("  d) Makes code easier to read")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Async is about not wasting time waiting.")
        print("While one task waits for a response, others can run.")
    else:
        print("Incorrect. The answer is b).")
        print("Async lets you overlap waiting time with useful work.")
        print("For CPU-heavy work, use multiprocessing instead.")
    print()

    # Question 2
    print("Question 2/7: What keyword makes a function into a coroutine?")
    print()
    print("  a) coroutine def")
    print("  b) async def")
    print("  c) await def")
    print("  d) def async")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! 'async def' defines a coroutine — a function")
        print("that can be paused and resumed.")
    else:
        print("Incorrect. The answer is b) async def.")
        print("The async keyword goes before def.")
    print()

    # Question 3
    print("Question 3/7: What does 'await' do?")
    print()
    print("  a) Stops the program completely")
    print("  b) Pauses the current coroutine until the awaited")
    print("     operation finishes, letting other coroutines run")
    print("  c) Runs a function in a new thread")
    print("  d) Deletes the coroutine")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! await pauses only the current coroutine.")
        print("The event loop runs other coroutines in the meantime.")
    else:
        print("Incorrect. The answer is b).")
        print("await is like saying 'I am waiting — go do something else")
        print("and come back to me when this is done.'")
    print()

    # Question 4
    print("Question 4/7: Why is time.sleep() bad in async code?")
    print()
    print("  a) It does not work at all")
    print("  b) It blocks the entire event loop, preventing all other")
    print("     coroutines from running")
    print("  c) It is too fast")
    print("  d) It raises an error")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! time.sleep() blocks everything.")
        print("Use await asyncio.sleep() instead — it only pauses the")
        print("current coroutine.")
    else:
        print("Incorrect. The answer is b).")
        print("time.sleep() is like the chef staring at the oven.")
        print("asyncio.sleep() is like the chef setting a timer and")
        print("working on other dishes.")
    print()

    # Question 5
    print("Question 5/7: What does asyncio.gather() do?")
    print()
    print("  a) Collects garbage")
    print("  b) Runs multiple coroutines concurrently and waits for")
    print("     all of them to finish")
    print("  c) Runs coroutines one at a time")
    print("  d) Cancels all running tasks")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! gather() starts all coroutines at once and returns")
        print("when every one of them has completed.")
    else:
        print("Incorrect. The answer is b).")
        print("gather(task_a(), task_b(), task_c()) runs all three")
        print("concurrently and collects their results.")
    print()

    # Question 6
    print("Question 6/7: What happens if you forget to use 'await'?")
    print()
    print("  result = some_async_function()")
    print()
    print("  a) The function runs normally")
    print("  b) You get a coroutine object instead of the actual result")
    print("  c) Python adds await automatically")
    print("  d) The program crashes immediately")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Without await, you get a coroutine object, not the")
        print("result. The function never actually runs to completion.")
    else:
        print("Incorrect. The answer is b).")
        print("Calling an async function without await returns a coroutine")
        print("object. You must await it to get the actual result.")
    print()

    # Question 7
    print("Question 7/7: Which of these is a GOOD fit for async?")
    print()
    print("  a) Calculating the first million prime numbers")
    print("  b) Making 100 HTTP requests to different APIs")
    print("  c) Processing a large image pixel by pixel")
    print("  d) Sorting a huge list of numbers")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Network I/O involves lots of waiting, which async")
        print("handles perfectly. CPU-heavy tasks (a, c, d) should use")
        print("multiprocessing instead.")
    else:
        print("Incorrect. The answer is b).")
        print("Async excels at I/O-bound work (network, files, databases).")
        print("CPU-bound work needs multiprocessing, not async.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand async/await fundamentals.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/async-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
