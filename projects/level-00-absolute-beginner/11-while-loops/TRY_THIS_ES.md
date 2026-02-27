# Prueba Esto — Ejercicio 11

1. Escribe un ciclo while que duplique un número hasta que supere 1000:
   ```python
   number = 1
   while number <= 1000:
       print(number)
       number = number * 2
   ```

2. Crea un verificador de contraseña que siga preguntando hasta que se ingrese la contraseña correcta:
   ```python
   correct = "python"
   attempt = ""
   while attempt != correct:
       attempt = input("Ingresa la contraseña: ")
   print("¡Bienvenido!")
   ```

3. Crea un ciclo infinito a propósito (un ciclo que nunca se detiene). Luego presiona Ctrl+C para detenerlo. Sentirte cómodo con Ctrl+C es importante — lo vas a necesitar cuando estés depurando.
   ```python
   while True:
       print("¡Esto nunca se va a detener solo!")
   ```

---

| [← Anterior](../10-for-loops/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../12-dictionaries/TRY_THIS_ES.md) |
|:---|:---:|---:|
