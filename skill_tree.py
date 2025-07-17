# skill_tree.py
"""
Skill tree module.
"""
class SkillTree:
    def __init__(self, base_skills):
        self.nodes = {}
        for skill, value in base_skills.items():
            self.nodes[skill] = {
                "level": 0,
                "max_level": 5,
                "cost": 1,
                "description": f"Increase {skill}"
            }
    def upgrade(self, skill):
        if skill in self.nodes:
            node = self.nodes[skill]
            if node["level"] < node["max_level"]:
                node["level"] += 1
                return True
        return False
    def get_node(self, skill):
        return self.nodes.get(skill, None)
    def __str__(self):
        lines = []
        for skill, data in self.nodes.items():
            lines.append(f"{skill.capitalize()}: Level {data['level']} / {data['max_level']}")
        return "\n".join(lines)
