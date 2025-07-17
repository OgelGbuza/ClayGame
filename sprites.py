# sprites.py
import pygame, math, random
import numpy as np
from resources import load_image_with_scale, load_sprite_sheet, get_asset_path
import config

# Helper to add slight noise to a surface so sprites look a bit more like
# handcrafted clay models.
def apply_clay_effect(surface: pygame.Surface):
    arr = pygame.surfarray.pixels3d(surface)
    noise = np.random.randint(-5, 6, arr.shape, dtype=np.int16)
    np.add(arr, noise, out=arr, casting="unsafe")
    np.clip(arr, 0, 255, out=arr)
    del arr


class ClaySprite(pygame.sprite.Sprite):
    """Base sprite class that applies small frame jitter."""

    def __init__(self):
        super().__init__()
        self._jitter = pygame.math.Vector2(0, 0)

    def apply_jitter(self, magnitude: int = 1):
        # remove previous jitter then apply a new random offset
        self.rect.move_ip(-self._jitter.x, -self._jitter.y)
        self._jitter.xy = (
            random.randint(-magnitude, magnitude),
            random.randint(-magnitude, magnitude),
        )
        self.rect.move_ip(self._jitter.x, self._jitter.y)

# ------------------------------
# AnimatedSprite Base Class
# ------------------------------
class AnimatedSprite(ClaySprite):
    def __init__(self, image_path, frame_width, frame_height, num_frames, animation_speed=150):
        super().__init__()
        # load_sprite_sheet returns a list of frames directly.
        self.frames = load_sprite_sheet(image_path, frame_width, frame_height, num_frames)
        for f in self.frames:
            apply_clay_effect(f)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

# ------------------------------
# ClaySoldier (Player)
# ------------------------------
class ClaySoldier(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Load idle frames from "player_idle.png" (4 frames, each 50x50)
        self.frames = load_sprite_sheet("player_idle.png", 50, 50, 4)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=pos)
        self.speed = 5
        self.animation_speed = 150  # milliseconds per frame
        self.last_update = pygame.time.get_ticks()

    def update(self, keys):
        # Movement using arrow keys
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Update animation
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now

# ------------------------------
# EnemyUnit (Static Russian Invader)
# ------------------------------
class EnemyUnit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50,50))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=pos)
        self.base_speed = 3
        self.speed = self.base_speed
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1

# ------------------------------
# BossEnemy (Boss)
# ------------------------------
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((80,80))
        self.image.fill((128,0,128))
        self.rect = self.image.get_rect(center=pos)
        self.base_speed = 2
        self.speed = self.base_speed
        self.direction = 1
        self.health = config.config["boss_health"]
        self.attack_timer = 0

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1

# ------------------------------
# AnimatedEnemy (Animated Russian Invader)
# ------------------------------
class AnimatedEnemy(AnimatedSprite):
    def __init__(self, pos):
        # Use "russian_invader.png" with 4 frames of 50x50, animation speed 200 ms
        super().__init__("russian_invader.png", 50, 50, 4, animation_speed=200)
        self.rect.center = pos
        self.base_speed = 2
        self.speed = self.base_speed
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1
        self.update_animation()

# ------------------------------
# Drone (Futuristic Ukrainian Drone)
# ------------------------------
class Drone(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image_with_scale("drone.png", (40,40))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 3
        self.amplitude = 20
        self.frequency = 0.05
        self.start_y = pos[1]
        self.counter = 0

    def update(self):
        self.rect.x += self.speed
        self.counter += 1
        self.rect.y = self.start_y + self.amplitude * math.sin(self.frequency * self.counter)
        if self.rect.left > 800:
            self.rect.right = 0

# ------------------------------
# PropagandaPoster (War Propaganda Parody)
# ------------------------------
class PropagandaPoster(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image_with_scale("propaganda_poster.png", (100,150))
        self.rect = self.image.get_rect(center=pos)

# ------------------------------
# Projectile (Fired by Player)
# ------------------------------
class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, speed=10):
        super().__init__()
        try:
            self.image = pygame.image.load(get_asset_path("weapon.png")).convert_alpha()
        except Exception as e:
            print("Error loading projectile image:", e)
            self.image = pygame.Surface((10,20), pygame.SRCALPHA)
            self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        # Debug: print position to check if moving
        # print("Projectile at:", self.rect)
        if self.rect.bottom < 0:
            self.kill()

# ------------------------------
# BossProjectile (Fired by Boss)
# ------------------------------
class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((15,15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255,255,0), (7,7), 7)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# ------------------------------
# PowerUp (Extra Life)
# ------------------------------
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()

# ------------------------------
# ShieldPowerUp (Temporary Shield)
# ------------------------------
class ShieldPowerUp(PowerUp):
    def __init__(self, pos):
        super().__init__(pos)
        self.image.fill((0,255,255))

# ------------------------------
# Explosion (Visual Effect)
# ------------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frame = 0
        self.max_frames = 20
        self.image = pygame.Surface((50,50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        self.update_image()

    def update_image(self):
        radius = int((self.frame / self.max_frames) * 40)
        self.image.fill((0,0,0,0))
        if radius > 0:
            alpha = 255 - int((self.frame / self.max_frames) * 255)
            color = (255,165,0,alpha)
            pygame.draw.circle(self.image, color, (25,25), radius)

    def update(self):
        self.frame += 1
        self.update_image()
        if self.frame >= self.max_frames:
            self.kill()

# ------------------------------
# ParallaxBackground (Scrolling Background)
# ------------------------------
class ParallaxBackground:
    def __init__(self, screen):
        self.screen = screen
        self.layer1 = load_image_with_scale("bg_layer1.png", (800,600))
        self.layer2 = load_image_with_scale("bg_layer2.png", (800,600))
        self.x1 = 0
        self.x2 = 0
        self.speed1 = 0.5
        self.speed2 = 1

    def update(self):
        self.x1 = (self.x1 - self.speed1) % self.layer1.get_width()
        self.x2 = (self.x2 - self.speed2) % self.layer2.get_width()

    def draw(self):
        sw = self.screen.get_width()
        for x in range(-self.layer1.get_width(), sw, self.layer1.get_width()):
            self.screen.blit(self.layer1, (x + self.x1, 0))
        for x in range(-self.layer2.get_width(), sw, self.layer2.get_width()):
            self.screen.blit(self.layer2, (x + self.x2, 0))

# ------------------------------
# Fortress (Strategic Building)
# ------------------------------
class Fortress(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image_with_scale("fortress.png", (200,150))
        self.rect = self.image.get_rect(center=pos)

# ------------------------------
# Village (Additional Building)
# ------------------------------
class Village(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image_with_scale("village.png", (150,100))
        self.rect = self.image.get_rect(center=pos)
