# Diagrams: Classes and Objects

[Back to concept](../classes-and-objects.md)

---

## Class Instantiation Sequence

When you create an object from a class, Python performs several steps behind the scenes.

```mermaid
sequenceDiagram
    participant Code as Your Code
    participant Class as Dog class
    participant Init as __init__ method
    participant Obj as New Object

    Code->>Class: Dog("Rex", 5)
    Note over Class: Python creates a<br/>new empty object
    Class->>Init: __init__(self, name, age)
    Note over Init: self.name = "Rex"
    Note over Init: self.age = 5
    Init-->>Class: Object is initialized
    Class-->>Code: Return the Dog object
    Note over Code: my_dog = Dog("Rex", 5)<br/>my_dog.name is "Rex"
```

## Inheritance Hierarchy

Child classes inherit attributes and methods from parent classes, and can add or override them.

```mermaid
classDiagram
    class Animal {
        +name: str
        +sound: str
        +speak() str
        +eat() str
    }

    class Dog {
        +breed: str
        +speak() str
        +fetch() str
    }

    class Cat {
        +indoor: bool
        +speak() str
        +purr() str
    }

    class GuideDog {
        +handler: str
        +guide() str
    }

    Animal <|-- Dog : inherits
    Animal <|-- Cat : inherits
    Dog <|-- GuideDog : inherits

    note for Dog "Overrides speak()&#10;Adds fetch()"
    note for GuideDog "Inherits from Dog&#10;AND from Animal"
```

## Method Resolution Order (MRO)

With multiple inheritance, Python searches for methods in a specific order called the MRO.

```mermaid
flowchart TD
    CALL["guide_dog.speak()"] --> STEP1{"1. GuideDog<br/>has speak()?"}
    STEP1 -->|No| STEP2{"2. Dog<br/>has speak()?"}
    STEP1 -->|Yes| FOUND1(["Use GuideDog.speak()"])
    STEP2 -->|Yes| FOUND2(["Use Dog.speak()"])
    STEP2 -->|No| STEP3{"3. Animal<br/>has speak()?"}
    STEP3 -->|Yes| FOUND3(["Use Animal.speak()"])
    STEP3 -->|No| STEP4{"4. object<br/>(base of everything)"}
    STEP4 -->|Not found| ERR["AttributeError!"]

    style STEP1 fill:#4a9eff,stroke:#2670c2,color:#fff
    style STEP2 fill:#51cf66,stroke:#27ae60,color:#fff
    style STEP3 fill:#ffd43b,stroke:#f59f00,color:#000
    style STEP4 fill:#cc5de8,stroke:#9c36b5,color:#fff
    style ERR fill:#ff6b6b,stroke:#c0392b,color:#fff
```

## Class vs Instance Attributes

Class attributes are shared by all objects. Instance attributes belong to one object.

```mermaid
flowchart TD
    subgraph CLASS ["Dog class"]
        CA["species = 'Canis familiaris'<br/>(shared by ALL dogs)"]
    end

    subgraph OBJ1 ["dog1 = Dog('Rex', 5)"]
        I1A["name = 'Rex'"]
        I1B["age = 5"]
    end

    subgraph OBJ2 ["dog2 = Dog('Bella', 3)"]
        I2A["name = 'Bella'"]
        I2B["age = 3"]
    end

    CLASS -->|"dog1.species"| OBJ1
    CLASS -->|"dog2.species"| OBJ2

    style CLASS fill:#ff922b,stroke:#e8590c,color:#fff
    style OBJ1 fill:#4a9eff,stroke:#2670c2,color:#fff
    style OBJ2 fill:#51cf66,stroke:#27ae60,color:#fff
```
