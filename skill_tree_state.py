# skill_tree_state.py
"""
Skill Tree State: displays a polished UI for upgrading skills.
Uses a gradient header and modern panel.
"""
import pygame
from skill_tree import SkillTree
from ui_helpers import draw_vertical_gradient


class SkillTreeState:
    def __init__(self, screen, player):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player = player
        if not hasattr(self.player, "skill_tree"):
            from HeroClassData import HeroClassData
            self.player.skill_tree = SkillTree(self.player.skills)
        self.skill_tree = self.player.skill_tree
        self.skill_points = self.player.skill_points
        self.options = list(self.skill_tree.nodes.keys())
        self.selection = 0
        self.font = pygame.font.SysFont("arial", 32)
        self.instruction = self.font.render("UP/DOWN: Navigate, ENTER: Upgrade, ESC: Exit", True, (255, 255, 255))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "playing"
                elif event.key == pygame.K_UP:
                    self.selection = (self.selection - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selection = (self.selection + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.skill_points > 0:
                        skill = self.options[self.selection]
                        if self.skill_tree.upgrade(skill):
                            self.skill_points -= self.skill_tree.nodes[skill]["cost"]
                            self.player.skills[skill] += 1
                            print(f"Upgraded {skill}: now {self.player.skills[skill]}")
                        else:
                            print(f"{skill.capitalize()} is already at maximum level.")
        return "skill_tree"

    def update(self):
        pass

    def draw(self):
        self.screen.fill((40, 40, 40))
        header = pygame.Surface((800, 80))
        draw_vertical_gradient(header, (50, 50, 100), (10, 10, 40))
        pygame.draw.rect(header, (255, 255, 255), header.get_rect(), 2)
        header_text = self.font.render("Skill Tree", True, (255, 255, 0))
        header.blit(header_text, (20, 20))
        self.screen.blit(header, (0, 0))
        sp_text = self.font.render(f"Skill Points: {self.skill_points}", True, (255, 215, 0))
        self.screen.blit(sp_text, (600, 20))
        panel = pygame.Surface((500, 400), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))
        pygame.draw.rect(panel, (255, 255, 255), panel.get_rect(), 2)
        self.screen.blit(panel, (250, 100))
        y = 140
        for i, skill in enumerate(self.options):
            node = self.skill_tree.get_node(skill)
            color = (255, 255, 0) if i == self.selection else (255, 255, 255)
            option_text = self.font.render(f"{skill.capitalize()}: Level {node['level']} / {node['max_level']}", True,
                                           color)
            self.screen.blit(option_text, (270, y))
            y += 50
        self.screen.blit(self.instruction, (260, 480))
        pygame.display.flip()
        self.clock.tick(60)
