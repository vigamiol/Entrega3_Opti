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
