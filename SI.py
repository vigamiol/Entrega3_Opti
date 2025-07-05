import random, math

class Problem:
    def __init__(self):
        # 5 medios: TV tarde, TV noche, Diario, Revista, Radio
        self.dim = 5
        # Dominios de cantidad de anuncios (xj)
        self.x_min = [0, 0, 0, 0, 0]
        self.x_max = [15, 10, 25, 4, 30]
        # Dominios de calidad (yj)
        self.y_min = [65, 90, 40, 60, 20]
        self.y_max = [85, 95, 60, 80, 30]
        # Costos (función de calidad)
        # c1 = 2*y1 + 30, c2 = 10*y2 - 600, c3 = 2*y3 - 40, c4 = y4 + 40, c5 = y5 - 10

    def get_costs(self, y):
        c = [
            2*y[0] + 30,
            10*y[1] - 600,
            2*y[2] - 40,
            y[3] + 40,
            y[4] - 10
        ]
        return c

    def check(self, x, y):
        # Restricciones de dominio
        for j in range(self.dim):
            if not (self.x_min[j] <= x[j] <= self.x_max[j]):
                return False
            if not (self.y_min[j] <= y[j] <= self.y_max[j]):
                return False

        c = self.get_costs(y)
        # Restricciones de costos
        if not (160 <= c[0] <= 200): return False
        if not (300 <= c[1] <= 350): return False
        if not (40 <= c[2] <= 80): return False
        if not (100 <= c[3] <= 120): return False
        if not (10 <= c[4] <= 20): return False

        # Restricciones adicionales
        if x[0]*c[0] + x[1]*c[1] > 3800: return False
        if x[2]*c[2] + x[3]*c[3] > 2800: return False
        if x[2]*c[2] + x[4]*c[4] > 3500: return False

        return True

    def fit(self, x, y):
        # Multiobjetivo: Max Z1 = sum(xj*yj), Min Z2 = sum(xj*cj)
        c = self.get_costs(y)
        valorizacion = sum([x[j]*y[j] for j in range(self.dim)])
        costo = sum([x[j]*c[j] for j in range(self.dim)])
        # Para un solo fitness, podemos ponderar: max(valor) - alpha*costo
        alpha = 0.01  # Peso para penalizar el costo
        return valorizacion - alpha * costo

    def random_solution(self):
        # Genera una solución aleatoria válida
        while True:
            x = [random.randint(self.x_min[j], self.x_max[j]) for j in range(self.dim)]
            y = [random.randint(self.y_min[j], self.y_max[j]) for j in range(self.dim)]
            if self.check(x, y):
                return x, y

    def keep_domain(self, x, j):
        # Mantener x en dominio (x es un número, no una lista)
        return max(self.x_min[j], min(self.x_max[j], int(round(x))))

    def keep_domain_y(self, y, j):
        # Mantener y en dominio (y es un número, no una lista)
        return max(self.y_min[j], min(self.y_max[j], int(round(y))))

class Individual:
    def __init__(self, p=None):
        self.p = p if p else Problem()
        self.dimension = self.p.dim
        self.x, self.y = self.p.random_solution()
        self.c = self.p.get_costs(self.y)

    def is_feasible(self):
        return self.p.check(self.x, self.y)

    def fitness(self):
        return self.p.fit(self.x, self.y)

    def is_better_than(self, other):
        return self.fitness() > other.fitness()

    def move(self, best, exploration_rate=0.2, mutation_rate=0.1):
        # Kookaburra: Explora o explota
        for j in range(self.dimension):
            if random.random() < exploration_rate:
                # Exploración: nuevo valor aleatorio
                self.x[j] = random.randint(self.p.x_min[j], self.p.x_max[j])
                self.y[j] = random.randint(self.p.y_min[j], self.p.y_max[j])
            else:
                # Explotación: muta alrededor del mejor
                self.x[j] = self.p.keep_domain(
                    best.x[j] + mutation_rate * random.gauss(0, 1), j)
                self.y[j] = self.p.keep_domain_y(
                    best.y[j] + mutation_rate * random.gauss(0, 1), j)
        # Actualizar costos después del movimiento
        self.c = self.p.get_costs(self.y)

    def copy(self, other):
        self.x = other.x.copy()
        self.y = other.y.copy()
        self.c = other.c.copy()

    def __str__(self):
        return f"x: {self.x}, y: {self.y}, c: {self.c}, fitness: {self.fitness():.2f}"

class Swarm:
    def __init__(self):
        self.max_iter = 100
        self.n_individual = 30
        self.exploration_rate = 0.2
        self.mutation_rate = 0.1
        self.swarm = []
        self.g = None
        self.p = Problem()

    def random(self):
        self.swarm = []
        for _ in range(self.n_individual):
            ind = Individual(self.p)
            self.swarm.append(ind)
        self.g = max(self.swarm, key=lambda ind: ind.fitness())
        self.show_results(0)

    def evolve(self):
        for t in range(1, self.max_iter + 1):
            # Ordenar por fitness descendente
            self.swarm.sort(key=lambda ind: ind.fitness(), reverse=True)
            self.g = self.swarm[0]
            for i in range(1, self.n_individual):
                ind = Individual(self.p)
                ind.copy(self.swarm[i])
                feasible = False
                tries = 0
                while not feasible and tries < 10:
                    ind.move(self.g, self.exploration_rate, self.mutation_rate)
                    feasible = ind.is_feasible()
                    tries += 1
                if feasible:
                    self.swarm[i].copy(ind)
            self.g = max(self.swarm, key=lambda ind: ind.fitness())
            self.show_results(t)

    def show_results(self, t):
        print(f"t: {t}, best_global: {self.g}")

    def optimizer(self):
        self.random()
        self.evolve()

# Ejecutar
if __name__ == "__main__":
    Swarm().optimizer()