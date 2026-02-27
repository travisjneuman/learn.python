"""Aprende a definir bloques de código reutilizables con parámetros y valores de retorno."""
# ============================================================
# Ejercicio 13: Funciones
# ============================================================
#
# Una función es un bloque de código reutilizable con un nombre.
# En vez de escribir el mismo código una y otra vez, lo pones
# en una función y la llamas cuando la necesites.
#
# Defines una función con "def", le das un nombre, y pones
# el código adentro (indentado).
# ============================================================

# Definir una función simple
def say_hello():
    print("¡Hola! Este mensaje viene de una función.")

# Llamar (usar) la función
say_hello()
say_hello()  # Puedes llamarla cuantas veces quieras

# Funciones con parámetros — valores que le pasas
def greet(name):
    print(f"¡Hola, {name}! Mucho gusto.")

greet("Alicia")
greet("Alicia")
greet("Roberto")

# Funciones que devuelven un valor
def add(a, b):
    result = a + b
    return result  # "return" envía el valor de vuelta a quien la llamó

total = add(5, 3)
print(f"5 + 3 = {total}")

# Puedes usar el valor devuelto directamente
print(f"10 + 20 = {add(10, 20)}")

# Funciones con valores por defecto
def make_greeting(name, greeting="Hola"):
    return f"¡{greeting}, {name}!"

print(make_greeting("Alicia"))              # Usa el valor por defecto: "Hola"
print(make_greeting("Alicia", "Hey"))       # Usa el proporcionado: "Hey"
print(make_greeting("Alicia", "Bienvenida"))  # Usa el proporcionado: "Bienvenida"

# Una función más práctica
def calculate_tip(meal_price, tip_percent=18):
    tip = meal_price * (tip_percent / 100)
    total = meal_price + tip
    return round(total, 2)

print()
print(f"Comida de $50, 18% de propina: ${calculate_tip(50)}")
print(f"Comida de $50, 20% de propina: ${calculate_tip(50, 20)}")
print(f"Comida de $75, 15% de propina: ${calculate_tip(75, 15)}")

# ============================================================
# POR QUÉ IMPORTAN LAS FUNCIONES:
#
# 1. Reutilización — escribe código una vez, úsalo muchas veces
# 2. Organización — divide problemas grandes en piezas pequeñas
# 3. Legibilidad — una función bien nombrada explica lo que hace
# 4. Pruebas — puedes probar cada función de forma independiente
#
# Si te encuentras copiando y pegando código, eso es una señal
# de que deberías ponerlo en una función.
# ============================================================
