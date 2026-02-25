"""
Quiz: Classes and Objects
Review: concepts/classes-and-objects.md
"""

from _quiz_helpers import normalize_answer


def run_quiz():
    print("=" * 60)
    print("  QUIZ: Classes and Objects")
    print("  Review: concepts/classes-and-objects.md")
    print("=" * 60)
    print()

    score = 0
    total = 7

    # Question 1
    print("Question 1/7: What is the relationship between a class")
    print("and an object?")
    print()
    print("  a) They are the same thing")
    print("  b) A class is a blueprint; an object is a thing created from it")
    print("  c) An object is a blueprint; a class is created from it")
    print("  d) Classes are for data; objects are for functions")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A class defines the structure. An object (instance)")
        print("is a concrete thing built from that structure.")
    else:
        print("Incorrect. The answer is b).")
        print("Think of a class as a cookie cutter and objects as cookies.")
    print()

    # Question 2
    print("Question 2/7: What does __init__ do?")
    print()
    print("  a) Deletes the object")
    print("  b) Prints the object")
    print("  c) Sets up the initial state when an object is created")
    print("  d) Imports the class")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! __init__ is the constructor. It runs automatically")
        print("when you create a new instance, setting up attributes.")
    else:
        print("Incorrect. The answer is c).")
        print("__init__ initializes the object's attributes when created.")
    print()

    # Question 3
    print("Question 3/7: What does 'self' refer to in a method?")
    print()
    print("  a) The class itself")
    print("  b) The specific object (instance) the method is called on")
    print("  c) The parent class")
    print("  d) Nothing — it is just a convention")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! self is the particular instance. When you call")
        print("my_dog.learn_trick('sit'), self is my_dog.")
    else:
        print("Incorrect. The answer is b).")
        print("self refers to the specific object the method was called on.")
    print()

    # Question 4
    print("Question 4/7: What error does this code produce?")
    print()
    print("  class Bad:")
    print("      def greet(name):")
    print('          return f"Hello {name}"')
    print()
    print("  b = Bad()")
    print('  b.greet("Alice")')
    print()
    print("  a) NameError")
    print("  b) SyntaxError")
    print("  c) TypeError — missing self parameter")
    print("  d) No error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "c":
        score += 1
        print("Correct! Every method needs self as its first parameter.")
        print("Python passes the instance automatically, but the method")
        print("must accept it.")
    else:
        print("Incorrect. The answer is c) TypeError.")
        print("Without self, Python passes the instance as 'name',")
        print("then 'Alice' has no parameter to go into.")
    print()

    # Question 5
    print("Question 5/7: What will this code print?")
    print()
    print("  class Cat:")
    print("      def __init__(self, name):")
    print("          self.name = name")
    print("      def speak(self):")
    print('          return f"{self.name} says Meow!"')
    print()
    print('  c = Cat("Whiskers")')
    print("  print(c.speak())")
    print()
    print('  a) "Cat says Meow!"')
    print('  b) "Whiskers says Meow!"')
    print('  c) "Meow!"')
    print("  d) Error")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! self.name was set to 'Whiskers' in __init__,")
        print("so speak() uses that value.")
    else:
        print('Incorrect. The answer is b) "Whiskers says Meow!".')
        print("The name attribute stores the value passed to __init__.")
    print()

    # Question 6
    print("Question 6/7: What is inheritance?")
    print()
    print("  a) When one object copies another object's data")
    print("  b) When a class builds on an existing class, gaining its")
    print("     attributes and methods")
    print("  c) When two classes share the same name")
    print("  d) When a function calls another function")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! A child class inherits from a parent class,")
        print("getting its methods and attributes, and can override them.")
    else:
        print("Incorrect. The answer is b).")
        print("Inheritance lets you create specialized versions of")
        print("existing classes without duplicating code.")
    print()

    # Question 7
    print("Question 7/7: Why is this default argument dangerous?")
    print()
    print("  class Bad:")
    print("      def __init__(self, items=[]):")
    print("          self.items = items")
    print()
    print("  a) Lists cannot be default arguments")
    print("  b) The same list is shared between ALL instances")
    print("  c) It causes a SyntaxError")
    print("  d) Nothing is wrong")
    print()
    answer = normalize_answer(input("Your answer: "))
    if answer == "b":
        score += 1
        print("Correct! Mutable defaults are shared. Use None as default")
        print("and create the list inside __init__: self.items = items or []")
    else:
        print("Incorrect. The answer is b).")
        print("The list object is created once and shared by all instances.")
        print("Use items=None, then self.items = items or [] inside __init__.")
    print()

    # Final score
    print("=" * 60)
    pct = round(score / total * 100)
    print(f"  Final Score: {score}/{total} ({pct}%)")
    print()
    if pct == 100:
        print("  Perfect! You understand classes and OOP fundamentals.")
    elif pct >= 70:
        print("  Good work! Review the questions you missed.")
    else:
        print("  Keep practicing! Re-read concepts/classes-and-objects.md")
        print("  and try again.")
    print("=" * 60)


if __name__ == "__main__":
    run_quiz()
