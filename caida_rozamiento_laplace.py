#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caída vertical con rozamiento lineal resuelta mediante Transformada de Laplace.

Ecuación del modelo (eje hacia abajo positivo):

    m * dv/dt = m*g - gamma * v

Dividiendo por m:

    dv/dt + (gamma/m) * v = g

Se resuelve usando Transformada de Laplace de forma simbólica con Sympy
y luego se evalúa numéricamente y se grafican una o varias curvas v(t)
en el mismo gráfico, según escenarios elegidos por el usuario.
"""

import sys

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# 1) Construcción simbólica de la solución con Transformada de Laplace
# ---------------------------------------------------------------------
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

    # V(s) = L{v(t)}(s)
    V = sp.Function("V")(s)

    # Ecuación en el dominio de Laplace:
    #   m*(s*V - v0) = m*g/s - gamma*V
    eq_L = sp.Eq(m * (s * V - v0), m * g / s - gamma * V)

    # Despejamos V(s)
    V_sol = sp.solve(eq_L, V)[0]

    # Transformada inversa de Laplace para obtener v(t)
    v_expr = sp.simplify(sp.inverse_laplace_transform(V_sol, s, t))

    return t, m, gamma, g, v0, v_expr


# ---------------------------------------------------------------------
# 2) Lectura de parámetros desde consola
# ---------------------------------------------------------------------
def leer_float(mensaje, default):
    txt = input(f"{mensaje} [{default}]: ").strip()
    if txt == "":
        return float(default)
    try:
        return float(txt)
    except ValueError:
        print("  Valor inválido, usando el valor por defecto.")
        return float(default)


def pedir_configuracion_global():
    """
    Pide parámetros globales de simulación (tiempo, cantidad de puntos)
    y cantidad de escenarios a simular.

    Retorna:
        t_max, n_puntos, n_escenarios
    """
    print("\n=== Configuración global de simulación ===")
    t_max = leer_float("Tiempo máximo de simulación T_max (s)", 10.0)
    n_puntos = int(leer_float("Cantidad de puntos para la simulación", 500))
    n_escenarios = int(leer_float("Cantidad de escenarios a simular", 1))

    if t_max <= 0:
        print("\nERROR: T_max debe ser positivo.")
        sys.exit(1)

    if n_puntos < 2:
        print("\nADVERTENCIA: n_puntos muy chico, usando 100.")
        n_puntos = 100

    if n_escenarios < 1:
        print("\nADVERTENCIA: cantidad de escenarios < 1, usando 1.")
        n_escenarios = 1

    return t_max, n_puntos, n_escenarios


def pedir_escenarios(n_escenarios):
    """
    Pide los parámetros físicos de cada escenario.

    Retorna:
        lista_escenarios: lista de dicts, cada uno con:
            {
                "nombre": str,
                "m": float,
                "gamma": float,
                "g": float,
                "v0": float
            }
    """
    escenarios = []
    print("\n=== Definición de escenarios ===")
    for i in range(n_escenarios):
        print(f"\nEscenario {i+1}:")
        nombre = input("Nombre/etiqueta del escenario (opcional): ").strip()
        if nombre == "":
            nombre = f"Escenario {i+1}"

        m_val = leer_float("  Masa m (kg)", 80.0)
        gamma_val = leer_float("  Coeficiente de rozamiento gamma (kg/s)", 12.0)
        g_val = leer_float("  Gravedad g (m/s^2)", 9.81)
        v0_val = leer_float("  Velocidad inicial v(0) (m/s)", 0.0)

        if m_val <= 0 or gamma_val <= 0:
            print("  ERROR: m y gamma deben ser positivos. Saliendo.")
            sys.exit(1)

        escenarios.append(
            {
                "nombre": nombre,
                "m": m_val,
                "gamma": gamma_val,
                "g": g_val,
                "v0": v0_val,
            }
        )

    return escenarios


# ---------------------------------------------------------------------
# 3) Función principal
# ---------------------------------------------------------------------
def main():
    # 1) Construimos la solución simbólica una sola vez
    print("Construyendo solución simbólica mediante Transformada de Laplace...")
    t, m, gamma, g, v0, v_expr = construir_solucion_simbolica()
    print("Solución simbólica v(t):")
    print(f"  v(t) = {v_expr}\n")

    # 2) Pedimos configuración global y escenarios
    t_max, n_puntos, n_escenarios = pedir_configuracion_global()
    escenarios = pedir_escenarios(n_escenarios)

    # 3) Convertimos la expresión simbólica a función numérica
    #    v_num(t, m, gamma, g, v0)
    v_num = sp.lambdify((t, m, gamma, g, v0), v_expr, "numpy")

    # 4) Vector de tiempos compartido por todos los escenarios
    t_vals = np.linspace(0.0, t_max, n_puntos)

    # 5) Gráfico
    plt.figure(figsize=(9, 5))

    print("\n=== Resultados por escenario ===")
    for esc in escenarios:
        nombre = esc["nombre"]
        m_val = esc["m"]
        gamma_val = esc["gamma"]
        g_val = esc["g"]
        v0_val = esc["v0"]

        # Evaluamos v(t) numéricamente
        v_vals = v_num(t_vals, m_val, gamma_val, g_val, v0_val)

        # Velocidad terminal para este escenario
        v_terminal = m_val * g_val / gamma_val

        print(f"\n{nombre}:")
        print(f"  m = {m_val} kg, gamma = {gamma_val} kg/s, g = {g_val} m/s^2, v0 = {v0_val} m/s")
        print(f"  Velocidad terminal v_T = m g / gamma = {v_terminal:.4f} m/s")
        print(f"  v({t_max}) = {v_vals[-1]:.4f} m/s")
        print(f"  |v(T_max) - v_T| = {abs(v_vals[-1] - v_terminal):.4e} m/s")

        # Curva de velocidad
        etiqueta_curva = f"{nombre} (m={m_val}, γ={gamma_val})"
        plt.plot(t_vals, v_vals, label=etiqueta_curva)

        # (Opcional) línea horizontal de velocidad terminal para cada escenario
        # Puede ensuciar el gráfico si hay muchos escenarios; activalo si querés.
        # plt.axhline(v_terminal, linestyle="--", alpha=0.4)

    plt.xlabel("t (s)")
    plt.ylabel("v(t) (m/s)")
    plt.title("Caída con rozamiento lineal - múltiples escenarios")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
