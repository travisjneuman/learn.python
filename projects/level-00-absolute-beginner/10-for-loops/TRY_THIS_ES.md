# Prueba Esto — Ejercicio 10

1. Imprime la tabla de multiplicar de un número:
   ```python
   number = 7
   for i in range(1, 11):
       print(f"{number} x {i} = {number * i}")
   ```

2. Recorre una lista de nombres y saluda a cada uno:
   ```python
   names = ["Alicia", "Roberto", "Carlos"]
   for name in names:
       print(f"¡Hola, {name}!")
   ```

3. Usa un ciclo for con `range()` para contar hacia atrás del 10 al 1:
   ```python
   for i in range(10, 0, -1):
       print(i)
   print("¡Despegue!")
   ```
   El tercer número en `range()` es el paso. `-1` significa contar hacia atrás.

---

| [← Anterior](../09-lists/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../11-while-loops/TRY_THIS_ES.md) |
|:---|:---:|---:|
