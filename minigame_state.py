"""Very small turn-based skirmish mode used as a proof of concept."""

import pygame
from sprites import ClaySoldier, EnemyUnit

GRID_SIZE = 64
GRID_WIDTH = 5
GRID_HEIGHT = 5


class MiniGameState:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player = ClaySoldier((GRID_SIZE // 2, GRID_SIZE // 2))
        self.enemy = EnemyUnit((GRID_SIZE * 4, GRID_SIZE * 4))
        self.turn = "player"

    def process_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if self.turn == "player" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.rect.y = max(0, self.player.rect.y - GRID_SIZE)
                    self.turn = "enemy"
                elif event.key == pygame.K_DOWN:
                    self.player.rect.y = min(GRID_SIZE*(GRID_HEIGHT-1), self.player.rect.y + GRID_SIZE)
                    self.turn = "enemy"
                elif event.key == pygame.K_LEFT:
                    self.player.rect.x = max(0, self.player.rect.x - GRID_SIZE)
                    self.turn = "enemy"
                elif event.key == pygame.K_RIGHT:
                    self.player.rect.x = min(GRID_SIZE*(GRID_WIDTH-1), self.player.rect.x + GRID_SIZE)
                    self.turn = "enemy"
        return None

    def update(self):
        if self.turn == "enemy":
            # simple enemy AI: move towards player one step
            if self.enemy.rect.x < self.player.rect.x:
                self.enemy.rect.x += GRID_SIZE
            elif self.enemy.rect.x > self.player.rect.x:
                self.enemy.rect.x -= GRID_SIZE
            elif self.enemy.rect.y < self.player.rect.y:
                self.enemy.rect.y += GRID_SIZE
            elif self.enemy.rect.y > self.player.rect.y:
                self.enemy.rect.y -= GRID_SIZE
            self.turn = "player"
        self.player.update(pygame.key.get_pressed())
        self.enemy.update()

    def draw(self):
        self.screen.fill((50, 50, 50))
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, (80, 80, 80), rect, 1)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)
        pygame.display.flip()
        self.clock.tick(60)
