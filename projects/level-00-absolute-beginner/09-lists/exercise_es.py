"""Aprende a crear, acceder, modificar y recorrer colecciones ordenadas usando listas."""
# ============================================================
# Ejercicio 09: Listas
# ============================================================
#
# Una lista es una colección ordenada de elementos.
# Piensa en ella como un estante numerado donde puedes guardar cosas.
# Las listas usan corchetes [] y los elementos se separan con comas.
# ============================================================

# Crear una lista
colors = ["rojo", "azul", "verde", "amarillo"]
print("Colores:", colors)

# Acceder a elementos por posición (se llama "índice").
# IMPORTANTE: Se cuenta desde 0, no desde 1.
print("Primer color:", colors[0])    # rojo
print("Segundo color:", colors[1])   # azul
print("Último color:", colors[-1])   # amarillo (-1 significa el último)

# ¿Cuántos elementos hay en la lista?
print("Número de colores:", len(colors))

# Agregar un elemento al final
colors.append("morado")
print("Después de agregar morado:", colors)

# Eliminar un elemento por su valor
colors.remove("azul")
print("Después de eliminar azul:", colors)

# Verificar si algo está en la lista
if "rojo" in colors:
    print("¡Rojo está en la lista!")

if "naranja" not in colors:
    print("Naranja NO está en la lista.")

# Las listas también pueden contener números
scores = [95, 87, 92, 78, 100]
print("Puntuaciones:", scores)
print("Mayor:", max(scores))
print("Menor:", min(scores))
print("Total:", sum(scores))
print("Promedio:", sum(scores) / len(scores))

# Las listas pueden contener una mezcla de tipos (pero generalmente se mantienen uniformes)
mixed = ["Alicia", 30, True, 3.14]
print("Lista mixta:", mixed)

# Ordenar una lista
numbers = [5, 2, 8, 1, 9, 3]
numbers.sort()
print("Ordenada:", numbers)

# ============================================================
# CONCEPTO CLAVE:
#
# Las listas son "mutables" — puedes cambiarlas después de crearlas.
# Esto es diferente de los strings, que no se pueden cambiar directamente.
# ============================================================
