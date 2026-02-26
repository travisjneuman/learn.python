"""
Quiz: Security Basics
Review: concepts/security-basics.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Security Basics")
    print("  Review: concepts/security-basics.md")
    print("=" * 60)
    print()

    score = 0
    total = 12

    # Question 1
    print("Question 1/12: What is SQL injection?")
    print()
    print("  a) A way to speed up database queries")
    print("  b) An attack where user input is treated as SQL code,")
    print("     allowing attackers to manipulate the database")
    print("  c) A method for inserting data into tables")
    print("  d) A type of database backup")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! SQL injection happens when user input is concatenated")
        print("into SQL queries without sanitization.")
    else:
        print("Incorrect. The answer is b).")
        print("Never build SQL queries with string concatenation on user input.")
    print()

    # Question 2
    print("Question 2/12: What is the primary defense against SQL injection?")
    print()
    print("  a) Input length limits")
    print("  b) Parameterized queries (using ? or %s placeholders)")
    print("  c) Encrypting the database")
    print("  d) Using HTTPS")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Parameterized queries tell the database to treat")
        print("values as data, never as SQL code.")
    else:
        print("Incorrect. The answer is b) parameterized queries.")
        print("Always use ? or %s placeholders, never string concatenation.")
    print()

    # Question 3
    print("Question 3/12: How should you store passwords?")
    print()
    print("  a) In plain text in the database")
    print("  b) Encrypted with a reversible cipher")
    print("  c) Hashed with bcrypt or argon2 (one-way, irreversible)")
    print("  d) In a .env file")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Hash passwords with bcrypt or argon2. Hashing is")
        print("one-way --- you verify by hashing the input and comparing.")
    else:
        print("Incorrect. The answer is c) hashed with bcrypt or argon2.")
        print("Never store passwords in plain text or with reversible encryption.")
    print()

    # Question 4
    print("Question 4/12: Where should you store API keys and secrets?")
    print()
    print("  a) In your Python source code")
    print("  b) In environment variables (loaded from .env locally)")
    print("  c) In a comment at the top of the file")
    print("  d) In the README")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Use environment variables for secrets.")
        print("Use .env files locally (never committed to git).")
    else:
        print("Incorrect. The answer is b) environment variables.")
    print()

    # Question 5
    print("Question 5/12: What should .gitignore include for security?")
    print()
    print("  a) .py files")
    print("  b) .env, *.pem, *.key, credentials.json")
    print("  c) README.md")
    print("  d) test files")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! .env files, private keys, and credential files must")
        print("never be committed to git.")
    else:
        print("Incorrect. The answer is b).")
        print("Always add secret files to .gitignore BEFORE your first commit.")
    print()

    # Question 6
    print("Question 6/12: What is Cross-Site Scripting (XSS)?")
    print()
    print("  a) Running Python scripts across different sites")
    print("  b) Injecting malicious JavaScript through user input that")
    print("     gets rendered as HTML")
    print("  c) Linking to external CSS files")
    print("  d) Cross-browser compatibility issues")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! XSS happens when user input is rendered as raw HTML,")
        print("allowing script injection. Use auto-escaping templates.")
    else:
        print("Incorrect. The answer is b).")
        print("Prevent XSS by using templates that auto-escape user content.")
    print()

    # Question 7
    print("Question 7/12: What is a path traversal attack?")
    print()
    print("  a) A user accessing different pages too quickly")
    print("  b) An attacker using ../../ in a filename to access files")
    print("     outside the intended directory")
    print("  c) A way to speed up file access")
    print("  d) Following symbolic links")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Path traversal uses relative paths to escape the")
        print("intended directory. Always validate with Path.resolve()")
        print("and is_relative_to().")
    else:
        print("Incorrect. The answer is b).")
        print("Always validate that resolved paths stay within the expected directory.")
    print()

    # Question 8
    print("Question 8/12: Why is client-side validation not enough for")
    print("security?")
    print()
    print("  a) Browsers do not support validation")
    print("  b) An attacker can bypass it completely --- always validate")
    print("     on the server")
    print("  c) It is too slow")
    print("  d) JavaScript is insecure")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Client-side validation improves UX but provides zero")
        print("security. An attacker can send requests directly to your server.")
    else:
        print("Incorrect. The answer is b).")
        print("Client-side validation is for UX. Server-side validation is for security.")
    print()

    # Question 9
    print("Question 9/12: What does pip-audit check for?")
    print()
    print("  a) Code style issues")
    print("  b) Known security vulnerabilities in your installed packages")
    print("  c) License compatibility")
    print("  d) Unused dependencies")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! pip-audit checks your dependencies against databases")
        print("of known CVEs (security vulnerabilities).")
    else:
        print("Incorrect. The answer is b).")
        print("Run pip-audit regularly to catch vulnerable dependencies.")
    print()

    # Question 10
    print("Question 10/12: What is CSRF (Cross-Site Request Forgery)?")
    print()
    print("  a) Faking a website's CSS")
    print("  b) Tricking a logged-in user into making an unintended request")
    print("     by exploiting their active session")
    print("  c) Forging SSL certificates")
    print("  d) Creating fake user accounts")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! CSRF exploits the fact that browsers automatically")
        print("send cookies. Protect with CSRF tokens in forms.")
    else:
        print("Incorrect. The answer is b).")
        print("CSRF tokens verify that form submissions come from your site.")
    print()

    # Question 11
    print("Question 11/12: What is wrong with logging passwords?")
    print()
    print("  a) Nothing --- logging is important")
    print("  b) Passwords in logs can be read by anyone with log access,")
    print("     creating a security breach")
    print("  c) It slows down the application")
    print("  d) The logger cannot handle passwords")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Never log sensitive data. Logs are often stored in")
        print("plain text and accessible to many people.")
    else:
        print("Incorrect. The answer is b).")
        print("Only log the username, never the password or other secrets.")
    print()

    # Question 12
    print("Question 12/12: What is the safe alternative to eval() for")
    print("parsing simple Python literals from user input?")
    print()
    print("  a) exec()")
    print("  b) ast.literal_eval()")
    print("  c) compile()")
    print("  d) json.loads()")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! ast.literal_eval() safely evaluates strings, numbers,")
        print("lists, and dicts without running arbitrary code.")
    else:
        print("Incorrect. The answer is b) ast.literal_eval().")
        print("It only parses simple Python literals --- no function calls,")
        print("no imports, no arbitrary code.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand Python security fundamentals.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/security-basics.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
