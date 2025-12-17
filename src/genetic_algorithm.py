import random
from src.neural_network import NeuralNetwork

class GeneticAlgorithm:
    """Genetic Algorithm to evolve bird brains"""
    
    def __init__(self, population_size=50, mutation_rate=0.1, mutation_strength=0.5):
        """
        Initialize genetic algorithm
        
        Args:
            population_size: Number of birds per generation
            mutation_rate: Probability of mutating each weight
            mutation_strength: Standard deviation of mutations
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.generation = 1
        self.best_fitness = 0
        self.best_brain = None
        
    def create_population(self):
        """Create initial population of neural networks"""
        return [NeuralNetwork() for _ in range(self.population_size)]
    
    def select_parents(self, population, fitness_scores):
        """
        Select parents for breeding using tournament selection
        
        Args:
            population: List of NeuralNetwork instances
            fitness_scores: List of fitness scores corresponding to population
        
        Returns:
            tuple: Two parent networks
        """
        tournament_size = 5
        
        def tournament():
            """Run a tournament to select one parent"""
            contestants = random.sample(list(zip(population, fitness_scores)), 
                                       min(tournament_size, len(population)))
            winner = max(contestants, key=lambda x: x[1])
            return winner[0]
        
        parent1 = tournament()
        parent2 = tournament()
        return parent1, parent2
    
    def evolve(self, population, fitness_scores):
        """
        Create next generation using genetic algorithm
        
        Args:
            population: List of NeuralNetwork instances
            fitness_scores: List of fitness scores
        
        Returns:
            list: New population of NeuralNetwork instances
        """
        if not fitness_scores:
            return self.create_population()
        
        # Track best performer
        max_fitness_idx = fitness_scores.index(max(fitness_scores))
        if fitness_scores[max_fitness_idx] > self.best_fitness:
            self.best_fitness = fitness_scores[max_fitness_idx]
            self.best_brain = population[max_fitness_idx].copy()
        
        new_population = []
        
        # Elitism - keep top 10% performers
        elite_count = max(1, self.population_size // 10)
        sorted_population = sorted(zip(population, fitness_scores), 
                                  key=lambda x: x[1], reverse=True)
        
        for i in range(elite_count):
            new_population.append(sorted_population[i][0].copy())
        
        # Create rest of population through crossover and mutation
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents(population, fitness_scores)
            
            # Crossover
            if random.random() < 0.8:  # 80% crossover rate
                child = parent1.crossover(parent2)
            else:
                child = parent1.copy()
            
            # Mutation
            child.mutate(self.mutation_rate, self.mutation_strength)
            
            new_population.append(child)
        
        self.generation += 1
        return new_population
    
    def get_stats(self, fitness_scores):
        """
        Get statistics about current generation
        
        Args:
            fitness_scores: List of fitness scores
        
        Returns:
            dict: Statistics including avg, max, min fitness
        """
        if not fitness_scores:
            return {
                'generation': self.generation,
                'avg_fitness': 0,
                'max_fitness': 0,
                'min_fitness': 0,
                'best_ever': self.best_fitness
            }
        
        return {
            'generation': self.generation,
            'avg_fitness': sum(fitness_scores) / len(fitness_scores),
            'max_fitness': max(fitness_scores),
            'min_fitness': min(fitness_scores),
            'best_ever': self.best_fitness
        }
