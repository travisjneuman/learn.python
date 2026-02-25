"""
Quiz: HTTP Explained
Review: concepts/http-explained.md
"""


def run_quiz():
    print("=" * 60)
    print("  QUIZ: HTTP Explained")
    print("  Review: concepts/http-explained.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What does HTTP stand for?")
    print()
    print("  a) Hyper Text Transfer Protocol")
    print("  b) High Tech Transfer Program")
    print("  c) Hyper Transfer Text Protocol")
    print("  d) Home Tool Transfer Protocol")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "a":
        score += 1
        print("Correct! HyperText Transfer Protocol is how browsers")
        print("and servers communicate.")
    else:
        print("Incorrect. The answer is a) HyperText Transfer Protocol.")
    print()

    # Question 2
    print("Question 2/7: Which HTTP method should you use to create")
    print("a new resource?")
    print()
    print("  a) GET")
    print("  b) POST")
    print("  c) DELETE")
    print("  d) PATCH")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! POST is used to create new resources.")
        print("GET reads, PUT replaces, PATCH updates, DELETE removes.")
    else:
        print("Incorrect. The answer is b) POST.")
        print("POST = create, GET = read, PUT = replace, DELETE = remove.")
    print()

    # Question 3
    print("Question 3/7: A server responds with status code 404.")
    print("What does that mean?")
    print()
    print("  a) The request was successful")
    print("  b) The server crashed")
    print("  c) The requested resource was not found")
    print("  d) You are not authorized")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! 404 means 'Not Found.' The URL you requested")
        print("does not exist on the server.")
    else:
        print("Incorrect. The answer is c) Not Found.")
        print("4xx errors are client errors. 404 specifically means the")
        print("resource does not exist at that URL.")
    print()

    # Question 4
    print("Question 4/7: What range of status codes indicates success?")
    print()
    print("  a) 1xx")
    print("  b) 2xx")
    print("  c) 3xx")
    print("  d) 4xx")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! 2xx = success (200 OK, 201 Created, etc.).")
        print("3xx = redirect, 4xx = client error, 5xx = server error.")
    else:
        print("Incorrect. The answer is b) 2xx.")
        print("200 OK and 201 Created are the most common success codes.")
    print()

    # Question 5
    print("Question 5/7: What format do most modern APIs use to")
    print("send and receive data?")
    print()
    print("  a) XML")
    print("  b) CSV")
    print("  c) JSON")
    print("  d) Plain text")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! JSON (JavaScript Object Notation) is the standard")
        print("data format for APIs. It maps directly to Python dicts.")
    else:
        print("Incorrect. The answer is c) JSON.")
        print("JSON looks like Python dictionaries and is easy to work with.")
    print()

    # Question 6
    print("Question 6/7: Why should you always set a timeout on")
    print("HTTP requests?")
    print()
    print("  a) To make the request faster")
    print("  b) So your program does not hang forever if the server")
    print("     is down or slow")
    print("  c) The server requires it")
    print("  d) Python will crash without it")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "b":
        score += 1
        print("Correct! Without a timeout, your program will wait")
        print("indefinitely if the server never responds.")
    else:
        print("Incorrect. The answer is b).")
        print("Always use requests.get(url, timeout=10) to avoid")
        print("hanging forever.")
    print()

    # Question 7
    print("Question 7/7: A status code of 500 means:")
    print()
    print("  a) The request was malformed (your fault)")
    print("  b) The resource was not found")
    print("  c) An internal server error occurred (their fault)")
    print("  d) The request was successful")
    print()
    answer = input("Your answer: ").strip().lower()
    if answer == "c":
        score += 1
        print("Correct! 5xx errors are server-side problems.")
        print("500 specifically means something went wrong on the server.")
    else:
        print("Incorrect. The answer is c).")
        print("5xx = server error. 4xx = client error (your fault).")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand HTTP fundamentals.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/http-explained.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
