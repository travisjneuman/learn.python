# Prueba Esto — Ejercicio 12

1. Crea un diccionario para tu película favorita con las claves: titulo, anio, director, calificacion. Imprime cada valor.

2. Crea un contador de palabras simple:
   ```python
   words = ["manzana", "banana", "manzana", "cereza", "banana", "manzana"]
   counts = {}
   for word in words:
       if word in counts:
           counts[word] = counts[word] + 1
       else:
           counts[word] = 1
   print(counts)
   ```

3. Intenta acceder a una clave que no existe (como `person["salary"]`). Lee el error. Luego prueba usar `.get()` que devuelve None en vez de fallar:
   ```python
   print(person.get("salary"))          # None
   print(person.get("salary", "N/A"))   # "N/A" (valor por defecto)
   ```

---

| [← Anterior](../11-while-loops/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../13-functions/TRY_THIS_ES.md) |
|:---|:---:|---:|
