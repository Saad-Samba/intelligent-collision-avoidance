import pygame
from src.game.game_settings import GameSettings, EvolutionSettings
from src.game.create_population import create_population
from src.game.obstacle import Rectangle

# game settings
pygame.init()
BACKGROUND_COLOUR = GameSettings.BACKGROUND_COLOUR
(WIDTH, HEIGHT) = GameSettings.WIDTH, GameSettings.HEIGHT
TARGET_LOCATION = GameSettings.TARGET_LOCATION
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GameSettings.CAPTION)
SCREEN.fill(BACKGROUND_COLOUR)

# GA hyperparameters
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
    pygame.draw.circle(SCREEN, (255, 10, 0), TARGET_LOCATION, 10, 0)
    # pygame.draw.rect(SCREEN, (0, 0, 255), (230, 200, 200, 200), 0)

agents = create_population(POPULATION_SIZE)
rect = Rectangle(125, 50, 100, 200, (0, 0, 255), 1)
rect2 = Rectangle(125, 360, 100, 10, (0, 0, 255), 2)
rect3 = Rectangle(125, 390, 100, 10, (0, 0, 255), 3)
rect4 = Rectangle(400, 330, 100, 10, (0, 0, 255), 4)
obstacles = [rect, rect2, rect3, rect4]
def run():
    """
    Begins the simulation
    """
    x_change = 0
    y_change = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -1
                elif event.key == pygame.K_RIGHT:
                    x_change = 1
                elif event.key == pygame.K_DOWN:
                    y_change = 1
                elif event.key == pygame.K_UP:
                    y_change = -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        static_environment()
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            # obstacle.move()
        for agent in agents:
            agent.move(x_change, y_change)
            agent.update(SCREEN, obstacles)
        pygame.display.update()


if __name__ == "__main__":
    run()
