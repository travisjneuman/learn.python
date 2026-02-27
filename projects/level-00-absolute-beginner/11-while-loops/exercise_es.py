"""Aprende a repetir acciones basándote en una condición usando ciclos while y break."""
# ============================================================
# Ejercicio 11: Ciclos While
# ============================================================
#
# Un ciclo while repite código mientras una condición sea True.
# "Mientras esto sea verdad, sigue haciendo esto."
#
# Los ciclos for son para "haz esto para cada elemento."
# Los ciclos while son para "sigue haciendo esto hasta que algo cambie."
# ============================================================

# Contar del 1 al 5 usando un ciclo while
count = 1

while count <= 5:
    print(f"El conteo es: {count}")
    count = count + 1  # ¡Esto es fundamental! Sin esto, el ciclo nunca termina.

print("¡Terminé de contar!")

# Una cuenta regresiva
print()
countdown = 5

while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("¡Ya!")

# Usar un ciclo while para validar la entrada del usuario
# (Esto sigue preguntando hasta que el usuario dé una respuesta válida)
print()
print("--- Juego de Adivinanzas ---")

secret = 7
guess = 0  # Empieza con un valor incorrecto para que el ciclo se ejecute al menos una vez

while guess != secret:
    guess = int(input("Adivina un número entre 1 y 10: "))
    if guess < secret:
        print("¡Muy bajo!")
    elif guess > secret:
        print("¡Muy alto!")

print("¡Lo adivinaste!")

# Usar "break" para salir de un ciclo antes de tiempo
print()
print("--- Escribe 'salir' para terminar ---")

while True:  # Este ciclo correría por siempre sin un break
    text = input("Di algo: ")
    if text == "salir":
        break  # Sale del ciclo inmediatamente
    print(f"Dijiste: {text}")

print("¡Hasta luego!")

# ============================================================
# ADVERTENCIA:
#
# Si olvidas cambiar la condición (como olvidar
# count = count + 1), el ciclo se ejecuta por siempre. Esto
# se llama un "ciclo infinito." Si esto pasa, presiona Ctrl+C
# en tu terminal para detener el programa.
# ============================================================
