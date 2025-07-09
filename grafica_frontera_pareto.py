import matplotlib.pyplot as plt
from SI import Swarm, Individual # Importamos las clases necesarias

# --- Funciones para la Frontera de Pareto (pueden estar aquí o en un util.py si se prefiere) ---
def dominates(ind1, ind2):
    # ind1 domina a ind2 si:
    # 1. ind1 es igual o mejor en todos los objetivos.
    # 2. ind1 es estrictamente mejor en al menos un objetivo.

    # Queremos maximizar valorizacion (ind1.valorizacion >= ind2.valorizacion)
    # Queremos minimizar costo (ind1.costo <= ind2.costo)

    cond1 = ind1.valorizacion >= ind2.valorizacion and ind1.costo <= ind2.costo
    cond2 = ind1.valorizacion > ind2.valorizacion or ind1.costo < ind2.costo

    return cond1 and cond2

def get_pareto_front(population):
    pareto_front = []
    for i in range(len(population)):
        is_dominated = False
        for j in range(len(population)):
            if i != j and dominates(population[j], population[i]):
                is_dominated = True
                break
        if not is_dominated:
            pareto_front.append(population[i])
    return pareto_front
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # 1. Ejecutar el optimizador Kookaburra
    print("Ejecutando el algoritmo Kookaburra...")
    optimizer = Swarm()
    optimizer.optimizer() # Esto ejecutará el algoritmo y llenará all_evaluated_solutions

    # 2. Obtener todas las soluciones exploradas y el mejor global (según fitness combinado)
    all_solutions_data = optimizer.all_evaluated_solutions
    best_global_individual = optimizer.g # El mejor individuo según el fitness combinado

    # 3. Convertir los datos explorados en objetos Individual para el cálculo de Pareto
    # Esto es necesario porque all_solutions_data solo tiene tuplas (valoracion, costo),
    # y la función dominates espera objetos Individual.
    # Si quieres la frontera de Pareto de TODAS las soluciones encontradas,
    # necesitarías almacenar los objetos Individual completos en Swarm.all_evaluated_solutions.
    # Para simplificar, vamos a generar la frontera de Pareto SOLO con los individuos finales en el enjambre.
    # O, si quieres de todos, la Swarm.all_evaluated_solutions debería guardar los objetos Individual.
    # Para el propósito de visualización, graficaremos todos los puntos y luego la frontera.

    # Opcion A: Frontera de Pareto de la población final del enjambre
    final_population = optimizer.swarm
    pareto_front_individuals = get_pareto_front(final_population)

    # Opcion B: (Más completa pero requiere almacenar más)
    # Si hubiéramos almacenado todos los objetos Individual en self.all_evaluated_solutions,
    # podríamos hacer pareto_front_individuals = get_pareto_front(optimizer.all_evaluated_solutions)
    # Pero como guardamos (valoracion, costo), solo podemos graficar los puntos.
    # Para obtener la frontera de TODOS los puntos, necesitaríamos una lista de todos los individuos
    # a lo largo de la ejecución. Vamos a usar la población final para la frontera por simplicidad.


    # 4. Preparar datos para la gráfica
    valorizaciones_exploradas = [sol[0] for sol in all_solutions_data]
    costos_explorados = [sol[1] for sol in all_solutions_data]

    # Datos del mejor global (según fitness combinado)
    best_val_combined = best_global_individual.valorizacion
    best_cost_combined = best_global_individual.costo

    # Datos de la Frontera de Pareto
    pareto_valorizaciones = [ind.valorizacion for ind in pareto_front_individuals]
    pareto_costos = [ind.costo for ind in pareto_front_individuals]
    
    # Ordenar la frontera de Pareto para que la línea se vea bien
    # Primero ordena por valorizacion, luego por costo para desempatar si es necesario
    pareto_points = sorted(zip(pareto_valorizaciones, pareto_costos), key=lambda x: x[0])
    pareto_valorizaciones_sorted = [p[0] for p in pareto_points]
    pareto_costos_sorted = [p[1] for p in pareto_points]


    # 5. Generar la gráfica
    plt.figure(figsize=(12, 8))

    # Puntos de todas las soluciones exploradas
    plt.scatter(valorizaciones_exploradas, costos_explorados, color='blue', alpha=0.3, label='Soluciones exploradas')

    # El mejor global encontrado por el algoritmo combinado
    plt.scatter([best_val_combined], [best_cost_combined], color='green', s=150, marker='*', zorder=5, label=f'Mejor global (fitness combinado)\nVal: {best_val_combined:.2f}, Cost: {best_cost_combined:.2f}')

    # Frontera de Pareto
    plt.plot(pareto_valorizaciones_sorted, pareto_costos_sorted, color='red', marker='o', linestyle='-', linewidth=2, markersize=8, label='Frontera de Pareto (Población final)')

    plt.title('Análisis de Frontera de Pareto: Valorización vs. Costo')
    plt.xlabel('Valorización (Objetivo a Maximizar)')
    plt.ylabel('Costo (Objetivo a Minimizar)')
    plt.grid(True)
    plt.legend()

    # Anotaciones para los ejes (opcional)
    if len(pareto_valorizaciones_sorted) > 1:
        # Punto con mayor valorización en la frontera de Pareto
        max_val_point = max(pareto_points, key=lambda x: x[0])
        # Punto con menor costo en la frontera de Pareto
        min_cost_point = min(pareto_points, key=lambda x: x[1])
        
        # Calcular offsets más seguros para el texto
        val_range = max(valorizaciones_exploradas) - min(valorizaciones_exploradas)
        cost_range = max(costos_explorados) - min(costos_explorados)
        
        plt.annotate('Mayor Valorización',
                     xy=max_val_point,  # Apuntar exactamente al punto con mayor valorización
                     xytext=(max_val_point[0] - val_range*0.2, max_val_point[1] + cost_range*0.1),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="k", lw=1, alpha=0.8),
                     fontsize=10, ha='center')

        plt.annotate('Menor Costo',
                     xy=min_cost_point,  # Apuntar exactamente al punto con menor costo
                     xytext=(min_cost_point[0] + val_range*0.1, min_cost_point[1] - cost_range*0.1),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", ec="k", lw=1, alpha=0.8),
                     fontsize=10, ha='center')


    plt.show()