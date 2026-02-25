"""
Quiz: API Basics
Review: concepts/api-basics.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: API Basics")
    print("  Review: concepts/api-basics.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What does API stand for?")
    print()
    print("  a) Advanced Programming Interface")
    print("  b) Application Programming Interface")
    print("  c) Automated Program Integration")
    print("  d) Application Process Integration")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Application Programming Interface — a way for")
        print("programs to talk to each other.")
    else:
        print("Incorrect. The answer is b) Application Programming Interface.")
    print()

    # Question 2
    print("Question 2/7: In REST, what HTTP method and URL pattern")
    print("would you use to get a specific user with ID 42?")
    print()
    print("  a) POST /users/42")
    print("  b) GET /users/42")
    print("  c) GET /users?id=42")
    print("  d) FETCH /users/42")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! GET /users/42 follows REST conventions.")
        print("The URL identifies the resource, GET reads it.")
    else:
        print("Incorrect. The answer is b) GET /users/42.")
        print("REST uses the URL path to identify resources and HTTP")
        print("methods to specify the action.")
    print()

    # Question 3
    print("Question 3/7: What does response.json() do in Python?")
    print()
    print("  a) Sends JSON to the server")
    print("  b) Parses the JSON response body into a Python dictionary")
    print("  c) Converts a dict to JSON")
    print("  d) Checks if the response is valid JSON")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! .json() parses the response body from JSON")
        print("into a Python dict (or list), so you can work with the data.")
    else:
        print("Incorrect. The answer is b).")
        print(".json() converts the JSON response into Python objects.")
    print()

    # Question 4
    print("Question 4/7: What status code indicates a new resource")
    print("was successfully created?")
    print()
    print("  a) 200")
    print("  b) 201")
    print("  c) 204")
    print("  d) 301")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! 201 Created is the standard response for")
        print("successful POST requests that create new resources.")
    else:
        print("Incorrect. The answer is b) 201 Created.")
        print("200 = OK (general success), 201 = Created (new resource).")
    print()

    # Question 5
    print("Question 5/7: Why is it bad practice to hardcode API URLs?")
    print()
    print('  requests.get("https://api.example.com/v2/users")')
    print()
    print("  a) It makes the code run slower")
    print("  b) If the URL changes, you have to find and update every")
    print("     occurrence throughout your code")
    print("  c) Python does not allow string URLs")
    print("  d) It is not bad practice")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Store the base URL in a variable or config.")
        print("That way you change it in one place if it ever changes.")
    else:
        print("Incorrect. The answer is b).")
        print("Use a variable: BASE_URL = 'https://api.example.com/v2'")
        print("then requests.get(f'{BASE_URL}/users').")
    print()

    # Question 6
    print("Question 6/7: What does response.raise_for_status() do?")
    print()
    print("  a) Prints the status code")
    print("  b) Returns the status code as a string")
    print("  c) Raises an exception if the response is a 4xx or 5xx error")
    print("  d) Sets the status code to 200")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! raise_for_status() throws an exception for error")
        print("responses, making it easy to catch failures.")
    else:
        print("Incorrect. The answer is c).")
        print("It is a convenient way to check for errors instead of")
        print("manually checking response.status_code.")
    print()

    # Question 7
    print("Question 7/7: What is the difference between an API key")
    print("and a Bearer token?")
    print()
    print("  a) They are the same thing")
    print("  b) An API key is a static secret string; a Bearer token")
    print("     is typically obtained by logging in and may expire")
    print("  c) API keys are more secure")
    print("  d) Bearer tokens do not work with Python")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! API keys are simple static secrets. Bearer tokens")
        print("(like JWTs) are obtained through authentication and often")
        print("have expiration times.")
    else:
        print("Incorrect. The answer is b).")
        print("API keys are static. Bearer tokens are dynamic and often")
        print("include user identity and expiration information.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand API fundamentals.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/api-basics.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
