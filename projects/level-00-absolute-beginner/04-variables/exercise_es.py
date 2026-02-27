"""Aprende a guardar valores en variables y usarlos en expresiones y sentencias print."""
# ============================================================
# Ejercicio 04: Variables
# ============================================================
#
# Una variable es un nombre que contiene un valor.
# Piensa en ella como una caja con etiqueta. Pones algo en la
# caja y usas la etiqueta para recuperarlo después.
#
# El signo = significa "guarda este valor en este nombre".
# NO significa "igual" como en la clase de matemáticas.
# Significa "pon lo de la derecha en el nombre de la izquierda".
# ============================================================

# Crea una variable llamada "name" y guarda el texto "Alicia" en ella.
name = "Alicia"

# Ahora podemos usar el nombre de la variable en vez de escribir el texto de nuevo.
print(name)

# Crea más variables.
age = 30
city = "Ciudad de México"

# Usa variables en sentencias print.
print("Nombre:", name)
print("Edad:", age)
print("Ciudad:", city)

# Puedes cambiar lo que contiene una variable en cualquier momento.
# El valor anterior se pierde. El nuevo valor lo reemplaza.
age = 31
print("El próximo año tendré", age)

# Puedes usar variables en operaciones matemáticas.
hours_per_day = 8
days_per_week = 5
hours_per_week = hours_per_day * days_per_week
print("Trabajo", hours_per_week, "horas por semana")

# Puedes combinar variables de texto (esto se llama "concatenación").
first_name = "Alicia"
last_name = "Neuman"
full_name = first_name + " " + last_name
print("Nombre completo:", full_name)

# ============================================================
# REGLAS PARA NOMBRES:
#
# Los nombres de variables pueden contener letras, números y guiones bajos.
# NO pueden empezar con un número.
# Son sensibles a mayúsculas: "Name" y "name" son variables diferentes.
# Usa minúsculas con guiones bajos para que sea legible: hours_per_week
# ============================================================
