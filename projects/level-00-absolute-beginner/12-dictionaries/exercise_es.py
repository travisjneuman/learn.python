"""Aprende a almacenar y recuperar datos etiquetados usando pares clave-valor en diccionarios."""
# ============================================================
# Ejercicio 12: Diccionarios
# ============================================================
#
# Un diccionario almacena datos como pares de clave-valor.
# Piensa en él como un diccionario real: buscas una palabra (clave)
# y obtienes su definición (valor).
#
# Las listas usan posiciones (índice 0, 1, 2...).
# Los diccionarios usan etiquetas (claves) para encontrar valores.
#
# Los diccionarios usan llaves {} y dos puntos entre clave:valor.
# ============================================================

# Crear un diccionario
person = {
    "name": "Alicia",
    "age": 30,
    "city": "Ciudad de México",
    "job": "Ingeniera"
}

# Acceder a un valor por su clave
print("Nombre:", person["name"])
print("Edad:", person["age"])

# Imprimir el diccionario completo
print("Persona completa:", person)

# Agregar un nuevo par clave-valor
person["hobby"] = "programar"
print("Después de agregar hobby:", person)

# Cambiar un valor existente
person["age"] = 31
print("Después de cumpleaños:", person)

# Eliminar un par clave-valor
del person["job"]
print("Después de eliminar trabajo:", person)

# Verificar si una clave existe
if "name" in person:
    print("El nombre está en el diccionario.")

if "salary" not in person:
    print("El salario NO está en el diccionario.")

# Recorrer un diccionario
print()
print("Toda la info de esta persona:")
for key, value in person.items():
    print(f"  {key}: {value}")

# Un ejemplo más práctico — una agenda telefónica
phone_book = {
    "Alicia": "555-0101",
    "Roberto": "555-0102",
    "Carlos": "555-0103"
}

name = "Roberto"
print(f"\nEl número de {name} es {phone_book[name]}")

# ============================================================
# CONCEPTO CLAVE:
#
# Usa una LISTA cuando tengas una colección ordenada de elementos similares.
#   Ejemplo: una lista de puntuaciones, una lista de nombres
#
# Usa un DICCIONARIO cuando tengas datos etiquetados.
#   Ejemplo: los datos de una persona, una configuración, una tabla de consulta
# ============================================================
