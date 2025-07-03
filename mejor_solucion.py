from SI import Swarm, Problem

if __name__ == "__main__":
    swarm = Swarm()
    swarm.optimizer()
    best = swarm.g
    p = swarm.p

    print("\n--- Mejor Solución Encontrada ---")
    print(f"x (cantidad anuncios): {best.x}")
    print(f"y (calidad anuncios): {best.y}")

    c = p.get_costs(best.y)
    print(f"c (costos individuales): {c}")

    valorizacion = sum([best.x[j]*best.y[j] for j in range(p.dim)])
    costo = sum([best.x[j]*c[j] for j in range(p.dim)])

    print(f"\nFunción a maximizar (valorización): {valorizacion}")
    print(f"Función a minimizar (costo): {costo}")

    print("\nCostos por medio:")
    for j in range(p.dim):
        print(f"  Medio {j+1}: costo = {c[j]}, calidad = {best.y[j]}")

    # Corroboración de restricciones monetarias
    print("\n--- Corroboración de restricciones monetarias ---")
    restr1 = best.x[0]*c[0] + best.x[1]*c[1]
    restr2 = best.x[2]*c[2] + best.x[3]*c[3]
    restr3 = best.x[2]*c[2] + best.x[4]*c[4]
    print(f"x1*c1 + x2*c2 = {restr1} (<= 3800): {'Cumple' if restr1 <= 3800 else 'No cumple'}")
    print(f"x3*c3 + x4*c4 = {restr2} (<= 2800): {'Cumple' if restr2 <= 2800 else 'No cumple'}")
    print(f"x3*c3 + x5*c5 = {restr3} (<= 3500): {'Cumple' if restr3 <= 3500 else 'No cumple'}")
