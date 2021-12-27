import pygame
from src.common.constants import SimulationSettings, EvolutionSettings
from src.game.create_population import create_population
from src.game.create_map import create_map
from src.learning.genetic import Genetic

#Simulation settings
pygame.init()
BACKGROUND_COLOUR = SimulationSettings.BACKGROUND_COLOUR
(WIDTH, HEIGHT) = SimulationSettings.WIDTH, SimulationSettings.HEIGHT
TARGET_LOCATION = SimulationSettings.TARGET_LOCATION
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(SimulationSettings.CAPTION)
SCREEN.fill(BACKGROUND_COLOUR)

# GA settings
POPULATION_SIZE = EvolutionSettings.POPULATION_SIZE
ELITISM = EvolutionSettings.ELITISM


def static_environment():
    """
    Sets up some static elements in the pygame environment
    such as the background colour, the map boundary and the target.
    """
    SCREEN.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(SCREEN, (255, 255, 255),
                     (10, 10, WIDTH - 20, HEIGHT - 20), 1)
    pygame.draw.circle(SCREEN, (255, 10, 0), TARGET_LOCATION, 10, 0)

agents = create_population(POPULATION_SIZE)

evolution = Genetic(
    agents,
    EvolutionSettings.ELITISM,
    EvolutionSettings.MUTATION_RATE,
    EvolutionSettings.POPULATION_SIZE
)

obstacles = create_map()

def run():
    """
    Begins the game
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        static_environment()
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.move()
        for agent in evolution.population:
            agent.move()
            agent.update(SCREEN, obstacles)
            agent.evaluate_fitness()
        if evolution.check_if_all_dead():
            evolution.make_next_generation()
        pygame.display.update()


if __name__ == "__main__":
    run()
