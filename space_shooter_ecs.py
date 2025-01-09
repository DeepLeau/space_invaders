import pygame
import os
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter ECS")

# Loading assets
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

# Simple Components
class Transform:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Renderable:
    def __init__(self, image):
        self.image = image
        self.mask = pygame.mask.from_surface(image)

class Health:
    def __init__(self, amount):
        self.max_health = amount
        self.current_health = amount

class Shooter:
    def __init__(self, laser_img):
        self.laser_img = laser_img
        self.cooldown = 30
        self.cooldown_counter = 0

class Enemy:
    pass

class Player:
    pass

class Laser:
    def __init__(self, velocity):
        self.velocity = velocity

# Entities
class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_type):
        return self.components.get(component_type)

# Game world
class World:
    def __init__(self):
        self.entities = []
        self.player = None
        self.score = 0
        self.level = 0
        self.lives = 5

    def create_player(self):
        player = Entity()
        player.add_component(Transform(WIDTH/2 - 50, HEIGHT - 100))
        player.add_component(Renderable(YELLOW_SPACE_SHIP))
        player.add_component(Health(100))
        player.add_component(Shooter(YELLOW_LASER))
        player.add_component(Player())
        self.player = player
        self.entities.append(player)

    def create_enemy(self, x, y, color):
        enemy = Entity()
        if color == "red":
            ship_img, laser_img = RED_SPACE_SHIP, RED_LASER
        elif color == "green":
            ship_img, laser_img = GREEN_SPACE_SHIP, GREEN_LASER
        else:
            ship_img, laser_img = BLUE_SPACE_SHIP, BLUE_LASER

        enemy.add_component(Transform(x, y))
        enemy.add_component(Renderable(ship_img))
        enemy.add_component(Health(100))
        enemy.add_component(Shooter(laser_img))
        enemy.add_component(Enemy())
        self.entities.append(enemy)

    def create_laser(self, x, y, img, velocity):
        laser = Entity()
        laser.add_component(Transform(x, y))
        laser.add_component(Renderable(img))
        laser.add_component(Laser(velocity))
        self.entities.append(laser)
        return laser

# Systems
class RenderSystem:
    @staticmethod
    def update(world):
        WIN.blit(BG, (0, 0))
        
        for entity in world.entities:
            transform = entity.get_component(Transform)
            renderable = entity.get_component(Renderable)
            if transform and renderable:
                WIN.blit(renderable.image, (transform.x, transform.y))
                
                # Affichage barre de vie pour joueur et ennemis
                health = entity.get_component(Health)
                if health:
                    health_ratio = health.current_health / health.max_health
                    pygame.draw.rect(WIN, (255,0,0), 
                                  (transform.x, transform.y + renderable.image.get_height() + 10,
                                   renderable.image.get_width(), 10))
                    pygame.draw.rect(WIN, (0,255,0),
                                  (transform.x, transform.y + renderable.image.get_height() + 10,
                                   renderable.image.get_width() * health_ratio, 10))

        # Score and health displayed
        font = pygame.font.SysFont("comicsans", 50)
        level_label = font.render(f"Niveau: {world.level}", 1, (255,255,255))
        lives_label = font.render(f"Vies: {world.lives}", 1, (255,255,255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

class MovementSystem:
    @staticmethod
    def update(world):
        keys = pygame.key.get_pressed()
        player = world.player
        if player:
            transform = player.get_component(Transform)
            renderable = player.get_component(Renderable)
            
            if keys[pygame.K_q] and transform.x - 5 > 0:  
                transform.x -= 5
            if keys[pygame.K_d] and transform.x + 5 + renderable.image.get_width() < WIDTH:  
                transform.x += 5
            if keys[pygame.K_z] and transform.y - 5 > 0:  
                transform.y -= 5
            if keys[pygame.K_s] and transform.y + 5 + renderable.image.get_height() < HEIGHT:  
                transform.y += 5
            if keys[pygame.K_SPACE]:
                shooter = player.get_component(Shooter)
                if shooter and shooter.cooldown_counter == 0:
                    world.create_laser(transform.x, transform.y, shooter.laser_img, -5)
                    shooter.cooldown_counter = 1

        # Enemies and laser movements
        for entity in world.entities[:]:
            if entity.get_component(Enemy):
                transform = entity.get_component(Transform)
                transform.y += 1
                
                if transform.y + 50 > HEIGHT:
                    world.lives -= 1
                    world.entities.remove(entity)
                    
                # Random ennemy shoot
                if random.randrange(0, 120) == 1:
                    shooter = entity.get_component(Shooter)
                    if shooter:
                        world.create_laser(transform.x, transform.y, shooter.laser_img, 5)

            # Laser movement
            laser = entity.get_component(Laser)
            if laser:
                transform = entity.get_component(Transform)
                transform.y += laser.velocity
                
                if transform.y < 0 or transform.y > HEIGHT:
                    world.entities.remove(entity)

class CollisionSystem:
    @staticmethod
    def update(world):
        player = world.player
        if not player:
            return

        player_transform = player.get_component(Transform)
        player_renderable = player.get_component(Renderable)

        # Collision system
        for entity in world.entities[:]:
            if entity == player:
                continue

            transform = entity.get_component(Transform)
            renderable = entity.get_component(Renderable)
            
            if not (transform and renderable):
                continue

            offset_x = int(transform.x - player_transform.x)
            offset_y = int(transform.y - player_transform.y)

            if player_renderable.mask.overlap(renderable.mask, (offset_x, offset_y)):
                if entity.get_component(Enemy):
                    world.entities.remove(entity)
                    player.get_component(Health).current_health -= 10
                elif entity.get_component(Laser):
                    if entity.get_component(Laser).velocity > 0:  
                        world.entities.remove(entity)
                        player.get_component(Health).current_health -= 10

        for entity in world.entities[:]:
            laser = entity.get_component(Laser)
            if laser and laser.velocity < 0:  
                laser_transform = entity.get_component(Transform)
                laser_renderable = entity.get_component(Renderable)

                for enemy in world.entities[:]:
                    if enemy.get_component(Enemy):
                        enemy_transform = enemy.get_component(Transform)
                        enemy_renderable = enemy.get_component(Renderable)

                        offset_x = int(enemy_transform.x - laser_transform.x)
                        offset_y = int(enemy_transform.y - laser_transform.y)

                        if laser_renderable.mask.overlap(enemy_renderable.mask, (offset_x, offset_y)):
                            world.entities.remove(enemy)  
                            world.entities.remove(entity)  
                            break

class CooldownSystem:
    @staticmethod
    def update(world):
        for entity in world.entities:
            shooter = entity.get_component(Shooter)
            if shooter:
                if shooter.cooldown_counter >= shooter.cooldown:
                    shooter.cooldown_counter = 0
                elif shooter.cooldown_counter > 0:
                    shooter.cooldown_counter += 1

class WaveSystem:
    @staticmethod
    def update(world):
        enemies = [e for e in world.entities if e.get_component(Enemy)]
        if not enemies:
            world.level += 1
            wave_length = 5 + world.level
            for _ in range(wave_length):
                x = random.randrange(50, WIDTH-100)
                y = random.randrange(-1500, -100)
                color = random.choice(["red", "blue", "green"])
                world.create_enemy(x, y, color)

def main():
    world = World()
    world.create_player()
    
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if world.lives <= 0 or (world.player and world.player.get_component(Health).current_health <= 0):
            running = False

        WaveSystem.update(world)
        MovementSystem.update(world)
        CollisionSystem.update(world)
        CooldownSystem.update(world)
        RenderSystem.update(world)
        
        pygame.display.update()

if __name__ == "__main__":
    main() 