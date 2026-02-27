"""Aprende a repetir acciones sobre secuencias y rangos usando ciclos for."""
# ============================================================
# Ejercicio 10: Ciclos For
# ============================================================
#
# Un ciclo for repite código una vez por cada elemento en una colección.
# "Para cada color en mi lista de colores, imprime ese color."
#
# Esta es una de las ideas más poderosas en la programación.
# En vez de escribir el mismo código 100 veces, lo escribes
# una vez y dejas que el ciclo lo repita.
# ============================================================

# Recorrer una lista de elementos
fruits = ["manzana", "banana", "cereza", "dátil"]

print("Mis frutas:")
for fruit in fruits:
    # Este código indentado se ejecuta una vez por cada fruta.
    # La variable "fruit" tiene un valor diferente cada vez.
    print(f"  - {fruit}")

# Recorrer números usando range()
# range(5) te da: 0, 1, 2, 3, 4
print()
print("Contando del 0 al 4:")
for number in range(5):
    print(number)

# range(1, 6) te da: 1, 2, 3, 4, 5
print()
print("Contando del 1 al 5:")
for number in range(1, 6):
    print(number)

# Usar un ciclo para calcular algo
scores = [85, 92, 78, 95, 88]
total = 0

for score in scores:
    total = total + score

average = total / len(scores)
print()
print(f"Puntuaciones: {scores}")
print(f"Total: {total}")
print(f"Promedio: {average}")

# Ciclo con una sentencia if adentro
print()
print("Números del 1 al 10 que son pares:")
for number in range(1, 11):
    if number % 2 == 0:
        print(f"  {number} es par")

# ============================================================
# CONCEPTO CLAVE:
#
# El nombre de variable después de "for" (como "fruit" o "number")
# lo eliges tú. Escoge algo descriptivo:
#   for student in students:
#   for file in files:
#   for item in shopping_list:
# ============================================================
