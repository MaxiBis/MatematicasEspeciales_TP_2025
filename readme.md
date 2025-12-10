# Trabajo Práctico – Matemáticas Especiales (UNTREF – 2025)

Este repositorio contiene material desarrollado para la asignatura **Matemáticas Especiales** de la carrera **Ingeniería en Computación**, correspondiente al año **2025**.

El eje principal del trabajo es el análisis y resolución, mediante **Transformada de Laplace**, de la ecuación diferencial que modela la **caída vertical con rozamiento lineal**, y su posterior implementación computacional con visualización gráfica.

---

## Requisitos

Para ejecutar los scripts de simulación se necesitan:

- **Python 3.10+** (recomendado).
- Librerías de Python:
  - `sympy`
  - `numpy`
  - `matplotlib`

Instalación rápida:

~~~bash
pip install sympy numpy matplotlib
~~~

---

## Ejecución

~~~bash
python caida_rozamiento_laplace_multi.py
~~~

---

## Diagrama de secuencia (Mermaid)

~~~mermaid
sequenceDiagram
    actor Usuario
    participant Programa as main()
    participant Sympy as Sympy<br/> (Laplace)
    participant Numpy as NumPy
    participant MPL as Matplotlib

    Usuario->>Programa: Ejecuta script (python caida_rozamiento_laplace_multi.py)

    Programa->>Sympy: construir_solucion_simbolica()
    Sympy-->>Programa: v_expr (solución simbólica v(t))

    Programa->>Usuario: Muestra v(t) simbólica
    Programa->>Usuario: Pide T_max, n_puntos, n_escenarios
    Usuario-->>Programa: Ingresa parámetros globales

    Programa->>Usuario: Pide datos de escenario 1..n
    loop Por cada escenario
        Usuario-->>Programa: Ingresa m, gamma, g, v0, nombre
        Programa->>Numpy: Genera t_vals = linspace(0, T_max, n_puntos)
        Programa->>Sympy: lambdify(v_expr) → v_num(...)
        Programa->>Numpy: Calcula v_vals = v_num(t_vals, m, gamma, g, v0)
        Programa->>Programa: Calcula v_T = m*g/gamma
        Programa->>Usuario: Imprime v_T, v(T_max), error
        Programa->>MPL: plot(t_vals, v_vals, label=escenario)
    end

    Programa->>MPL: Configura labels, título, leyenda, grid
    Programa->>MPL: show()
    MPL-->>Usuario: Muestra gráfico con todas las curvas v(t)
~~~
