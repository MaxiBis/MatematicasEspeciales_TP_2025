#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caída vertical con rozamiento lineal resuelta mediante Transformada de Laplace.

Ecuación del modelo (eje hacia abajo positivo):

    m * dv/dt = m*g - gamma * v

Dividiendo por m:

    dv/dt + (gamma/m) * v = g

Se resuelve usando Transformada de Laplace de forma simbólica con Sympy
y luego se evalúa numéricamente y se grafica v(t).
"""

import sys

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


def construir_solucion_simbolica():
    """
    Construye la solución simbólica v(t) usando Transformada de Laplace.

    EDO en v(t):
        dv/dt + (gamma/m) * v = g,   v(0) = v0

    En Laplace:
        m*(s*V(s) - v0) = m*g/s - gamma*V(s)

    Retorna:
        t, m, gamma, g, v0, v_expr
    donde v_expr es la expresión simbólica de v(t).
    """
    # Símbolos
    t, s = sp.symbols("t s", real=True, positive=True)
    m, gamma, g, v0 = sp.symbols("m gamma g v0", positive=True)

    # V(s) será la transformada de Laplace de v(t)
    V = sp.Function("V")(s)

    # Ecuación en el dominio de Laplace:
    # m*(s*V - v0) = m*g/s - gamma*V
    eq_L = sp.Eq(m * (s * V - v0), m * g / s - gamma * V)

    # Despejamos V(s)
    V_sol = sp.solve(eq_L, V)[0]

    # Transformada inversa de Laplace para obtener v(t)
    v_expr = sp.simplify(sp.inverse_laplace_transform(V_sol, s, t))

    return t, m, gamma, g, v0, v_expr


def pedir_parametros_usuario():
    """
    Pide por consola los parámetros físicos y numéricos al usuario.

    Retorna:
        m_val, gamma_val, g_val, v0_val, t_max, n_puntos
    """
    print("=== Modelo: caída vertical con rozamiento lineal ===")
    print("Ecuación: m dv/dt = m g - gamma v")
    print("Se asume eje hacia abajo positivo.\n")

    def leer_float(mensaje, default):
        txt = input(f"{mensaje} [{default}]: ").strip()
        if txt == "":
            return float(default)
        try:
            return float(txt)
        except ValueError:
            print("  Valor inválido, usando el valor por defecto.")
            return float(default)

    m_val = leer_float("Masa m (kg)", 80.0)
    gamma_val = leer_float("Coeficiente de rozamiento gamma (kg/s)", 12.0)
    g_val = leer_float("Gravedad g (m/s^2)", 9.81)
    v0_val = leer_float("Velocidad inicial v(0) (m/s)", 0.0)
    t_max = leer_float("Tiempo máximo de simulación T_max (s)", 10.0)
    n_puntos = int(leer_float("Cantidad de puntos para la simulación", 500))

    if m_val <= 0 or gamma_val <= 0:
        print("\nERROR: m y gamma deben ser positivos.")
        sys.exit(1)

    if t_max <= 0:
        print("\nERROR: T_max debe ser positivo.")
        sys.exit(1)

    if n_puntos < 2:
        print("\nADVERTENCIA: n_puntos muy chico, usando 100.")
        n_puntos = 100

    return m_val, gamma_val, g_val, v0_val, t_max, n_puntos


def main():
    # 1) Construimos la solución simbólica una sola vez
    print("Construyendo solución simbólica mediante Transformada de Laplace...")
    t, m, gamma, g, v0, v_expr = construir_solucion_simbolica()
    print("Solución simbólica v(t):")
    print(f"  v(t) = {v_expr}\n")

    # 2) Pedimos parámetros al usuario
    m_val, gamma_val, g_val, v0_val, t_max, n_puntos = pedir_parametros_usuario()

    # 3) Convertimos la expresión simbólica a función numérica
    #    v_num(t, m, gamma, g, v0)
    v_num = sp.lambdify((t, m, gamma, g, v0), v_expr, "numpy")

    # 4) Construimos el vector de tiempos y evaluamos v(t)
    t_vals = np.linspace(0.0, t_max, n_puntos)
    v_vals = v_num(t_vals, m_val, gamma_val, g_val, v0_val)

    # 5) Velocidad terminal
    v_terminal = m_val * g_val / gamma_val

    # 6) Información por consola
    print("\n=== Resultados ===")
    print(f"Velocidad terminal teórica v_T = m g / gamma = {v_terminal:.4f} m/s")
    print(f"Velocidad al final de la simulación v({t_max}) = {v_vals[-1]:.4f} m/s")
    print(f"Diferencia |v(T_max) - v_T| = {abs(v_vals[-1] - v_terminal):.4e} m/s\n")

    # 7) Gráfico
    plt.figure(figsize=(8, 5))
    plt.plot(t_vals, v_vals, label="v(t)")
    plt.axhline(v_terminal, linestyle="--", label=f"v_T = {v_terminal:.2f} m/s")
    plt.xlabel("t (s)")
    plt.ylabel("v(t) (m/s)")
    plt.title("Caída con rozamiento lineal - velocidad vs tiempo")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
