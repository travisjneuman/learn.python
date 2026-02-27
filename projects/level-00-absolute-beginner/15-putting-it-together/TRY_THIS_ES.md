# Prueba Esto — Ejercicio 15

1. Agrega una funcionalidad que permita al usuario agregar un nuevo estudiante. Pide el nombre y la puntuación, luego vuelve a imprimir el reporte.

2. Crea tu propio archivo de datos con diferentes estudiantes y puntuaciones. Haz que el script lea de tu archivo en vez del original.

3. Agrega una funcionalidad que imprima solo los estudiantes que sacaron menos de 80 (estudiantes que necesitan ayuda extra):
   ```python
   print("\nEstudiantes por debajo de 80:")
   for student in students:
       if student["score"] < 80:
           print(f"  {student['name']}: {student['score']}")
   ```

4. Si te sientes ambicioso: guarda el reporte en un archivo nuevo en vez de solo imprimirlo. Pista:
   ```python
   with open("reporte.txt", "w") as f:
       f.write("Reporte de Estudiantes\n")
       f.write("Nombre, Puntuación, Calificación\n")
       for student in students:
           grade = get_letter_grade(student["score"])
           f.write(f"{student['name']}, {student['score']}, {grade}\n")
   ```

---

| [← Anterior](../14-reading-files/TRY_THIS_ES.md) | [Inicio](../../../README.md) | [Siguiente →](../README_ES.md) |
|:---|:---:|---:|
