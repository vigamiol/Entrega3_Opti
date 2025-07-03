import matplotlib.pyplot as plt
from SI import Swarm

class SwarmWithHistory(Swarm):
    def __init__(self):
        super().__init__()
        self.history = []

    def show_results(self, t):
        # Guarda el fitness del mejor global en cada iteración
        self.history.append(self.g.fitness())
        # Opcional: imprime cada 50 iteraciones
        if t % 50 == 0 or t == 0 or t == self.max_iter:
            print(f"t: {t}, best_global: {self.g}")

if __name__ == "__main__":
    swarm = SwarmWithHistory()
    swarm.optimizer()
    plt.plot(swarm.history, marker='o', linestyle='-')
    plt.xlabel('Iteración')
    plt.ylabel('Fitness del mejor individuo')
    plt.title('Evolución del Fitness por Iteración')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
