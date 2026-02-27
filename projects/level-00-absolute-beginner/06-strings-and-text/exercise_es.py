"""Aprende a crear, combinar, formatear y manipular cadenas de texto (strings)."""
# ============================================================
# Ejercicio 06: Strings y Texto
# ============================================================
#
# Un "string" es cualquier texto dentro de comillas.
# Los strings son una de las cosas más comunes con las que vas a trabajar.
# ============================================================

# Crear strings
greeting = "Hola"
name = "Alicia"

# Combinar strings (concatenación) — los pega uno con otro
message = greeting + ", " + name + "!"
print(message)

# f-strings — la forma moderna y limpia de poner variables dentro del texto.
# Pon una f antes de la comilla de apertura, y luego usa {nombre_variable} adentro.
print(f"Hola, {name}! Bienvenida a Python.")

# Puedes poner cualquier expresión dentro de las llaves.
age = 30
print(f"{name} tiene {age} años.")
print(f"En 10 años, {name} tendrá {age + 10}.")

# Longitud de un string — cuántos caracteres tiene (incluyendo espacios)
sentence = "Python es divertido"
print(f"La oración '{sentence}' tiene {len(sentence)} caracteres.")

# Mayúsculas y minúsculas
print("hola".upper())     # HOLA
print("HOLA".lower())     # hola
print("hola".title())     # Hola

# Verificar qué contiene un string
email = "usuario@ejemplo.com"
print(f"¿El email contiene @? {'@' in email}")

# Reemplazar texto
old_text = "Me gusta Java"
new_text = old_text.replace("Java", "Python")
print(new_text)

# Dividir un string en una lista de palabras
words = "uno dos tres cuatro".split()
print(words)

# ============================================================
# CONCEPTO CLAVE:
#
# Los strings son "inmutables" — no puedes cambiarlos directamente.
# Cuando llamas a .upper() o .replace(), Python crea un NUEVO
# string. El original no cambia a menos que lo reasignes.
# ============================================================
