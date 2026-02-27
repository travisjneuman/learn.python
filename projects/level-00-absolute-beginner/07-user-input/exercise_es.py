"""Aprende a leer la entrada del usuario desde el teclado y convertirla al tipo de dato correcto."""
# ============================================================
# Ejercicio 07: Entrada del Usuario
# ============================================================
#
# La función input() pausa tu programa y espera a que el
# usuario escriba algo. Lo que sea que escriba se convierte
# en un string.
#
# Así es como haces programas interactivos.
# ============================================================

# Pregunta el nombre del usuario. El texto dentro de input() es
# el mensaje que el usuario ve.
name = input("¿Cómo te llamas? ")

# Ahora usa lo que escribieron.
print(f"¡Mucho gusto, {name}!")

# Pregunta su color favorito.
color = input("¿Cuál es tu color favorito? ")
print(f"{color} es un gran color.")

# IMPORTANTE: input() siempre te da un string, incluso si el
# usuario escribe un número. Si quieres hacer operaciones
# matemáticas con él, debes convertirlo.

age_text = input("¿Cuántos años tienes? ")

# Convierte el string a un número usando int()
age = int(age_text)

# Ahora puedes hacer operaciones matemáticas con él.
print(f"El próximo año vas a tener {age + 1}.")

# Puedes hacer la conversión en una sola línea:
# age = int(input("¿Cuántos años tienes? "))

# ============================================================
# ERROR COMÚN:
#
# Si el usuario escribe algo que no es un número (como "abc")
# y tú intentas int("abc"), Python va a fallar con un ValueError.
# Por ahora, solo escribe números válidos. Más adelante
# aprenderás a manejar entradas incorrectas de forma elegante.
# ============================================================
