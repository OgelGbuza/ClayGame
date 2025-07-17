#generate_assets.py

import pygame, os, math, random, struct, wave


pygame.init()

# Set up the assets folder.
assets_dir = "assets"
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def save_asset(surface, filename):
    path = os.path.join(assets_dir, filename)
    pygame.image.save(surface, path)
    print(f"Saved {path}")

# ---------------------
# Utility: Generate Radial Gradient Circle (remains useful)
def generate_gradient_circle(radius, color_center, color_edge):
    """Generate a circular Surface with a radial gradient."""
    size = radius * 2
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        t = r / radius  # 1 at center, 0 at edge
        color = (
            int(color_center[0]*t + color_edge[0]*(1-t)),
            int(color_center[1]*t + color_edge[1]*(1-t)),
            int(color_center[2]*t + color_edge[2]*(1-t)),
            255
        )
        pygame.draw.circle(surf, color, (radius, radius), r)
    return surf

# ---------------------
# Utility: Add Pixel Noise (new utility for detailed textures)
def add_pixel_noise(surf, intensity=20):
    """Adds subtle pixel noise to a Surface for texture."""
    width, height = surf.get_size()
    for _ in range(width * height // intensity):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        color = surf.get_at((x,y))
        offset = random.randint(-10, 10)
        noisy_color = (
            max(0, min(255, color[0] + offset)),
            max(0, min(255, color[1] + offset)),
            max(0, min(255, color[2] + offset)),
            color[3]
        )
        surf.set_at((x,y), noisy_color)
    return surf


# ---------------------
# Common Font for text rendering (smaller, pixel-art style font)
font = pygame.font.Font(pygame.font.get_default_font(), 10)

# --------------------- Detailed Hero Assets ---------------------
def generate_detailed_ukrainian_soldier():
    surf = pygame.Surface((32,32), pygame.SRCALPHA) # Soldier sprite, same size
    # Enhanced color palette - more depth and variation
    color_body_base = (85, 90, 70)
    color_body_shade = (70, 75, 55)
    color_helmet_base = (95, 100, 80)
    color_helmet_shade = (80, 85, 65)
    color_details = (45, 45, 45)
    skin_color = (210, 190, 160)
    skin_shadow = (180, 160, 130)
    outline_color = (20, 20, 20) # Define outline color

    # Body - more defined shape with shading and outline
    pygame.draw.rect(surf, outline_color, (7-1, 4-1, 18+2, 20+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (7, 4, 18, 20)) # Body base
    pygame.draw.polygon(surf, color_body_shade, [(7, 4), (16, 2), (25, 4), (25, 24), (7, 24)]) # Body shading

    # Legs - outlined legs
    pygame.draw.rect(surf, outline_color, (7-1, 24-1, 6+2, 7+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (7, 24, 6, 7)) # Left Leg
    pygame.draw.rect(surf, color_body_shade, (7, 31, 6, 1)) # Leg shading
    pygame.draw.rect(surf, outline_color, (19-1, 24-1, 6+2, 7+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (19, 24, 6, 7)) # Right Leg
    pygame.draw.rect(surf, color_body_shade, (19, 31, 6, 1)) # Leg shading

    # Arms - outlined arms
    pygame.draw.rect(surf, outline_color, (3-1, 6-1, 4+2, 9+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (3, 6, 4, 9)) # Left Arm
    pygame.draw.rect(surf, color_body_shade, (3, 6, 1, 9)) # Arm shading
    pygame.draw.rect(surf, outline_color, (25-1, 6-1, 4+2, 9+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (25, 6, 4, 9)) # Right Arm
    pygame.draw.rect(surf, color_body_shade, (28, 6, 1, 9)) # Arm shading

    # Head and Helmet - detailed helmet and face with outline
    pygame.draw.circle(surf, outline_color, (16, 4), 5) # Face outline
    pygame.draw.circle(surf, skin_color, (16, 4), 4) # Face base
    pygame.draw.circle(surf, skin_shadow, (17, 5), 3) # Face shadow
    pygame.draw.polygon(surf, outline_color, [(3-1, 0), (29+1, 0), (31+1, 4), (1-1, 4)], 1) # Helmet outline
    pygame.draw.polygon(surf, color_helmet_base, [(3, 0), (29, 0), (31, 4), (1, 4)]) # Helmet base
    pygame.draw.polygon(surf, color_helmet_shade, [(3, 0), (16, -2), (29, 0), (29, 4), (3, 4)]) # Helmet shading

    # Weapon - more detailed rifle with outline
    pygame.draw.rect(surf, outline_color, (1-1, 9-1, 9+2, 2+2), 1) # Outline
    pygame.draw.rect(surf, color_details, (1, 9, 9, 2)) # Gun stock
    pygame.draw.rect(surf, outline_color, (10-1, 7-1, 12+2, 4+2), 1) # Outline
    pygame.draw.rect(surf, color_details, (10, 7, 12, 4)) # Gun body
    pygame.draw.rect(surf, outline_color, (22-1, 7-1, 6+2, 2+2), 1) # Outline
    pygame.draw.rect(surf, color_details, (22, 7, 6, 2)) # Gun barrel

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

ukrainian_soldier = generate_detailed_ukrainian_soldier()
save_asset(ukrainian_soldier, "ukrainian_soldier.png")

def generate_detailed_russian_soldier():
    surf = pygame.Surface((32,32), pygame.SRCALPHA) # Soldier sprite, same size
    # Enhanced color palette - more depth, khaki tones
    color_body_base = (95, 90, 75)
    color_body_shade = (80, 75, 60)
    color_helmet_base = (105, 100, 85)
    color_helmet_shade = (90, 85, 70)
    color_details = (55, 50, 45)
    skin_color = (220, 200, 170)
    skin_shadow = (190, 170, 140)
    outline_color = (20, 20, 20) # Define outline color

    # Body - similar structure to Ukrainian, different shading and outline
    pygame.draw.rect(surf, outline_color, (7-1, 4-1, 18+2, 20+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (7, 4, 18, 20)) # Body base
    pygame.draw.polygon(surf, color_body_shade, [(7, 4), (16, 2), (25, 4), (25, 24), (7, 24)]) # Body shading - same shape

    # Legs - outlined legs
    pygame.draw.rect(surf, outline_color, (7-1, 24-1, 6+2, 7+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (7, 24, 6, 7)) # Left Leg
    pygame.draw.rect(surf, color_body_shade, (7, 31, 6, 1)) # Leg shading
    pygame.draw.rect(surf, outline_color, (19-1, 24-1, 6+2, 7+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (19, 24, 6, 7)) # Right Leg
    pygame.draw.rect(surf, color_body_shade, (19, 31, 6, 1)) # Leg shading

    # Arms - outlined arms
    pygame.draw.rect(surf, outline_color, (3-1, 6-1, 4+2, 9+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (3, 6, 4, 9)) # Left Arm
    pygame.draw.rect(surf, color_body_shade, (3, 6, 1, 9)) # Arm shading
    pygame.draw.rect(surf, outline_color, (25-1, 6-1, 4+2, 9+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (25, 6, 4, 9)) # Right Arm
    pygame.draw.rect(surf, color_body_shade, (28, 6, 1, 9)) # Arm shading

    # Head and Helmet - slightly different helmet, subtle face details with outline
    pygame.draw.circle(surf, outline_color, (16, 4), 5) # Face outline
    pygame.draw.circle(surf, skin_color, (16, 4), 4) # Face base
    pygame.draw.circle(surf, skin_shadow, (15, 5), 3) # Face shadow - different side
    pygame.draw.polygon(surf, outline_color, [(3-1, 0), (29+1, 0), (32+1, 5), (0-1, 5)], 1) # Helmet outline
    pygame.draw.polygon(surf, color_helmet_base, [(3, 0), (29, 0), (32, 5), (0, 5)]) # Helmet base - different shape
    pygame.draw.polygon(surf, color_helmet_shade, [(3, 0), (16, -2), (29, 0), (29, 5), (3, 5)]) # Helmet shading

    # Weapon - rifle on different side with outline
    pygame.draw.rect(surf, outline_color, (22-1, 9-1, 9+2, 2+2), 1) # Outline
    pygame.draw.rect(surf, color_details, (22, 9, 9, 2)) # Gun stock - different side
    pygame.draw.rect(surf, outline_color, (10-1, 7-1, 12+2, 4+2), 1) # Outline
    pygame.draw.rect(surf, color_details, (10, 7, 12, 4)) # Gun body - same
    pygame.draw.rect(surf, outline_color, (4-1, 7-1, 6+2, 2+2), 1) # Outline
    pygame.draw.rect(surf, color_details, (4, 7, 6, 2)) # Gun barrel - different side

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

russian_soldier = generate_detailed_russian_soldier()
save_asset(russian_soldier, "russian_soldier.png")


def generate_detailed_character(char_code, base_color): # More detailed characters
    surf = pygame.Surface((32,32), pygame.SRCALPHA) # Character sprite, same size
    # Enhanced color variations
    color_light = base_color
    color_shade = (base_color[0] * 0.75, base_color[1] * 0.75, base_color[2] * 0.75) # Darker shade
    outline_color = (20, 20, 20) # Define outline color

    # Body - more refined humanoid shape with shading and outline
    pygame.draw.rect(surf, outline_color, (7-1, 3-1, 18+2, 22+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (7, 3, 18, 22), border_radius=2) # Body base
    pygame.draw.polygon(surf, color_shade, [(7, 3), (16, 1), (25, 3), (25, 25), (7, 25)]) # Body shading

    # Legs - outlined legs
    pygame.draw.rect(surf, outline_color, (7-1, 25-1, 6+2, 6+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (7, 25, 6, 6)) # Left Leg
    pygame.draw.rect(surf, color_shade, (7, 31, 6, 1)) # Leg shading
    pygame.draw.rect(surf, outline_color, (19-1, 25-1, 6+2, 6+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (19, 25, 6, 6)) # Right Leg
    pygame.draw.rect(surf, color_shade, (19, 31, 6, 1)) # Leg shading

    # Arms - outlined arms
    pygame.draw.rect(surf, outline_color, (3-1, 5-1, 4+2, 9+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (3, 5, 4, 9)) # Left Arm
    pygame.draw.rect(surf, color_shade, (3, 5, 1, 9)) # Arm shading
    pygame.draw.rect(surf, outline_color, (25-1, 5-1, 4+2, 9+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (25, 5, 4, 9)) # Right Arm
    pygame.draw.rect(surf, color_shade, (28, 5, 1, 9)) # Arm shading

    # Head - darker, shading as head with outline
    pygame.draw.circle(surf, outline_color, (16, 3), 5) # Head outline
    pygame.draw.circle(surf, color_shade, (16, 3), 4) # Head - darker, shading as head

    # Class-specific details - more elaborate
    if char_code == "M": # Mage - staff more detailed
        pygame.draw.rect(surf, outline_color, (26-1, 4-1, 2+2, 14+2), 1) # Outline
        pygame.draw.rect(surf, (180, 180, 255), (26, 4, 2, 14)) # Staff base
        pygame.draw.circle(surf, outline_color, (27, 3), 4) # Staff top outline
        pygame.draw.circle(surf, (200, 200, 255), (27, 3), 3) # Staff top
    elif char_code == "R": # Rogue - hood more defined with outline
        pygame.draw.polygon(surf, outline_color, [(3-1, 1), (29+1, 1), (27+1, 5), (5-1, 5)], 1) # Hood outline
        pygame.draw.polygon(surf, color_shade, [(3, 1), (29, 1), (27, 5), (5, 5)]) # Hood shape
    elif char_code == "E": # Engineer - goggles more detailed with outline
        pygame.draw.rect(surf, outline_color, (10-1, 1-1, 12+2, 3+2), 1) # Goggles frame outline
        pygame.draw.rect(surf, (150, 150, 150), (10, 1, 12, 3), border_radius=1) # Goggles frame
        pygame.draw.rect(surf, (180, 180, 200), (12, 2, 3, 1)) # Goggle lens highlight
        pygame.draw.rect(surf, (180, 180, 200), (17, 2, 3, 1)) # Goggle lens highlight
    elif char_code == "A": # Artist - beret more detailed with outline
        pygame.draw.circle(surf, outline_color, (16, 1), 7) # Beret base outline
        pygame.draw.circle(surf, (200, 100, 100), (16, 1), 6) # Beret base
        pygame.draw.circle(surf, (180, 80, 80), (15, 0), 5) # Beret detail

    # Text label - slightly more stylized
    txt_color = (0,0,0) if sum(base_color) > 300 else (255,255,255) # Contrast color
    txt = font.render(char_code, True, txt_color)
    txt_scaled = pygame.transform.scale(txt, (int(txt.get_width()*1.3), int(txt.get_height()*1.3))) # Slightly larger text
    surf.blit(txt_scaled, txt_scaled.get_rect(center=(16,16+4))) # Shift text down

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

mage = generate_detailed_character("M", (150,50,200))
save_asset(mage, "mage.png")
rogue = generate_detailed_character("R", (50,150,50))
save_asset(rogue, "rogue.png")
engineer = generate_detailed_character("E", (100,100,150))
save_asset(engineer, "engineer.png")
artist = generate_detailed_character("A", (200,150,200))
save_asset(artist, "artist.png")

# --------------------- Detailed Equipment Assets ---------------------
def generate_detailed_weapon(): # More detailed Rifle/Assault Rifle
    surf = pygame.Surface((32, 12), pygame.SRCALPHA) # Weapon sprite - slightly taller
    color_gun_metal = (90, 90, 90)
    color_gun_dark = (50, 50, 50)
    color_gun_detail = (70, 70, 70)
    outline_color = (20, 20, 20) # Define outline color

    # Stock - more defined stock with outline
    pygame.draw.rect(surf, outline_color, (0-1, 5-1, 8+2, 2+2), 1) # Outline
    pygame.draw.rect(surf, color_gun_metal, (0, 5, 8, 2))
    pygame.draw.polygon(surf, color_gun_metal, [(0, 5), (2, 3), (8, 3), (8, 7)]) # Stock shape
    pygame.draw.rect(surf, color_gun_detail, (1, 6, 6, 1)) # Stock detail line

    # Body - more detailed body with magazine and outline
    pygame.draw.rect(surf, outline_color, (8-1, 3-1, 16+2, 6+2), 1) # Outline
    pygame.draw.rect(surf, color_gun_metal, (8, 3, 16, 6)) # Body base
    pygame.draw.rect(surf, color_gun_dark, (8, 5, 16, 4)) # Darker center
    pygame.draw.rect(surf, color_gun_detail, (12, 4, 8, 1)) # Body detail line
    pygame.draw.rect(surf, outline_color, (24-1, 3-1, 3+2, 5+2), 1) # Outline
    pygame.draw.rect(surf, color_gun_dark, (24, 3, 3, 5), border_radius=1) # Magazine

    # Barrel - more defined barrel with sight and outline
    pygame.draw.rect(surf, outline_color, (27-1, 5-1, 5+2, 2+2), 1) # Outline
    pygame.draw.rect(surf, color_gun_dark, (27, 5, 5, 2)) # Barrel base
    pygame.draw.rect(surf, color_gun_metal, (27, 3, 3, 2)) # Sight on top

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

weapon_asset = generate_detailed_weapon()
weapon_surface = pygame.Surface((32, 32), pygame.SRCALPHA) # Square surface for weapon
weapon_surface.blit(weapon_asset, ((32 - weapon_asset.get_width())//2, (32 - weapon_asset.get_height())//2 + 10)) # Center, shift down
save_asset(weapon_surface, "weapon.png")


def generate_detailed_armor(): # More detailed Flak Jacket/Body Armor
    surf = pygame.Surface((32,32), pygame.SRCALPHA) # Armor sprite, same size
    color_armor_base = (130, 130, 130)
    color_armor_shade = (100, 100, 100)
    color_armor_detail = (150, 150, 150)
    outline_color = (20, 20, 20) # Define outline color

    # Main body armor - more layered look with outline
    pygame.draw.rect(surf, outline_color, (3-1, 1-1, 26+2, 30+2), 1) # Outline
    pygame.draw.rect(surf, color_armor_base, (3, 1, 26, 30), border_radius=3) # Base shape
    pygame.draw.polygon(surf, color_armor_shade, [(3, 1), (16, -1), (29, 1), (29, 31), (3, 31)]) # Overall shading
    pygame.draw.rect(surf, color_armor_detail, (6, 4, 20, 6)) # Top plate
    pygame.draw.rect(surf, color_armor_detail, (6, 12, 20, 6)) # Middle plate
    pygame.draw.rect(surf, color_armor_detail, (6, 20, 20, 6)) # Bottom plate

    # Side details - straps/pouches with outline
    pygame.draw.rect(surf, outline_color, (1-1, 6-1, 2+2, 8+2), 1) # Outline
    pygame.draw.rect(surf, color_armor_shade, (1, 6, 2, 8)) # Left strap
    pygame.draw.rect(surf, outline_color, (29-1, 6-1, 2+2, 8+2), 1) # Outline
    pygame.draw.rect(surf, color_armor_shade, (29, 6, 2, 8)) # Right strap

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

armor_asset = generate_detailed_armor()
save_asset(armor_asset, "armor.png")


def generate_detailed_accessory(): # More detailed Binoculars
    surf = pygame.Surface((32,32), pygame.SRCALPHA) # Accessory sprite, same size
    color_lens_base = (50, 50, 150) # Blueish lens
    color_lens_highlight = (80, 80, 180)
    color_body_base = (100, 100, 100)
    color_body_shade = (70, 70, 70)
    outline_color = (20, 20, 20) # Define outline color

    # Binocular bodies - more defined shapes with outlines
    pygame.draw.ellipse(surf, outline_color, (4-1, 12-1, 12+2, 16+2), 1) # Outline
    pygame.draw.ellipse(surf, color_body_base, (4, 12, 12, 16)) # Left body
    pygame.draw.ellipse(surf, color_body_shade, (4, 12, 6, 16)) # Left body shading
    pygame.draw.ellipse(surf, outline_color, (16-1, 12-1, 12+2, 16+2), 1) # Outline
    pygame.draw.ellipse(surf, color_body_base, (16, 12, 12, 16)) # Right body
    pygame.draw.ellipse(surf, color_body_shade, (22, 12, 6, 16)) # Right body shading

    # Lenses - with highlights and outlines
    pygame.draw.circle(surf, outline_color, (10, 16), 7) # Left lens outline
    pygame.draw.circle(surf, color_lens_base, (10, 16), 6) # Left lens base
    pygame.draw.circle(surf, color_lens_highlight, (9, 15), 3) # Left lens highlight
    pygame.draw.circle(surf, outline_color, (22, 16), 7) # Right lens outline
    pygame.draw.circle(surf, color_lens_base, (22, 16), 6) # Right lens base
    pygame.draw.circle(surf, color_lens_highlight, (21, 15), 3) # Right lens highlight

    # Connecting bridge - more detailed with outline
    pygame.draw.rect(surf, outline_color, (10-1, 11-1, 12+2, 6+2), 1) # Outline
    pygame.draw.rect(surf, color_body_base, (10, 11, 12, 6)) # Bridge base
    pygame.draw.polygon(surf, color_body_shade, [(10, 11), (16, 9), (22, 11), (22, 17), (10, 17)]) # Bridge shading

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

accessory_asset = generate_detailed_accessory()
save_asset(accessory_asset, "accessory.png")


# --------------------- Detailed NPC Assets ---------------------
def generate_detailed_npc(char_code, base_color): # More detailed NPCs
    surf = pygame.Surface((32,32), pygame.SRCALPHA) # NPC sprite, same size
    # Enhanced color variations - more shades
    color_light = base_color
    color_base = (base_color[0] * 0.85, base_color[1] * 0.85, base_color[2] * 0.85) # Base shade
    color_shade = (base_color[0] * 0.7, base_color[1] * 0.7, base_color[2] * 0.7) # Darker shade
    outline_color = (20, 20, 20) # Define outline color

    # Body - more defined humanoid shape with layered shading and outline
    pygame.draw.rect(surf, outline_color, (7-1, 3-1, 18+2, 22+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (7, 3, 18, 22), border_radius=2) # Body light
    pygame.draw.polygon(surf, color_base, [(7, 3), (16, 1), (25, 3), (25, 25), (7, 25)]) # Body base shade
    pygame.draw.polygon(surf, color_shade, [(7, 3), (16, 1), (25, 3), (25, 25), (16, 25), (7, 25)]) # Body darker shade

    # Legs - outlined legs
    pygame.draw.rect(surf, outline_color, (7-1, 25-1, 6+2, 6+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (7, 25, 6, 6)) # Left Leg
    pygame.draw.rect(surf, color_shade, (7, 31, 6, 1)) # Leg shading
    pygame.draw.rect(surf, outline_color, (19-1, 25-1, 6+2, 6+2), 1) # Outline
    pygame.draw.rect(surf, color_light, (19, 25, 6, 6)) # Right Leg
    pygame.draw.rect(surf, color_shade, (19, 31, 6, 1)) # Leg shading

    # Head - darker with outline
    pygame.draw.circle(surf, outline_color, (16, 3), 5) # Head outline
    pygame.draw.circle(surf, color_shade, (16, 3), 4) # Head - darker

    # NPC-specific details - more elaborate
    if char_code == "E": # Elder - cane more detailed with outline
        pygame.draw.rect(surf, outline_color, (5-1, 24-1, 2+2, 8+2), 1) # Outline
        pygame.draw.rect(surf, (120, 80, 40), (5, 24, 2, 8)) # Cane base
        pygame.draw.rect(surf, (100, 60, 30), (4, 24, 2, 6)) # Cane detail
        pygame.draw.circle(surf, outline_color, (6, 24), 3) # Cane top outline
        pygame.draw.circle(surf, (120, 80, 40), (6, 24), 2) # Cane top
    elif char_code == "Q": # Quest Master - scroll more detailed with outline
        pygame.draw.rect(surf, outline_color, (23-1, 5-1, 7+2, 7+2), 1) # Outline
        pygame.draw.rect(surf, (200, 200, 150), (23, 5, 7, 7)) # Scroll base
        pygame.draw.polygon(surf, (180, 180, 130), [(23, 5), (26, 3), (30, 5), (30, 12), (23, 12)]) # Scroll detail
        for y_offset in [0, 1, 2]: # Scroll lines
            pygame.draw.line(surf, (100, 100, 80), (24, 7 + y_offset), (29, 7 + y_offset), 1)


    # Text label - slightly more stylized
    txt_color = (0,0,0) if sum(base_color) > 300 else (255,255,255) # Contrast color
    txt = font.render(char_code, True, txt_color)
    txt_scaled = pygame.transform.scale(txt, (int(txt.get_width()*1.3), int(txt.get_height()*1.3))) # Slightly larger text
    surf.blit(txt_scaled, txt_scaled.get_rect(center=(16,16+4))) # Shift text down

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=15)

    return surf

elder = generate_detailed_npc("E", (120,100,80))
save_asset(elder, "elder.png")
quest_master = generate_detailed_npc("Q", (150,80,150))
save_asset(quest_master, "quest_master.png")


elder_portrait = pygame.Surface((64,64), pygame.SRCALPHA) # Portrait, same size
# Portrait - even more detailed face with outline
face_color_base = (100, 80, 60)
face_color_shade = (70, 50, 30)
outline_color = (20, 20, 20) # Define outline color

pygame.draw.circle(elder_portrait, outline_color, (32, 32), 29) # Face outline
pygame.draw.circle(elder_portrait, face_color_base, (32, 32), 28) # Face base
pygame.draw.circle(elder_portrait, face_color_shade, (35, 35), 25) # Face shading
pygame.draw.circle(elder_portrait, outline_color, (32, 32), 28, 1) # Border
pygame.draw.circle(elder_portrait, outline_color, (24, 24), 4) # Left eye outline
pygame.draw.circle(elder_portrait, (0,0,0), (24, 24), 3) # Left eye
pygame.draw.circle(elder_portrait, outline_color, (40, 24), 4) # Right eye outline
pygame.draw.circle(elder_portrait, (0,0,0), (40, 24), 3) # Right eye
pygame.draw.rect(elder_portrait, outline_color, (28-1, 40-1, 8+2, 2+2), 1) # Mouth outline
pygame.draw.rect(elder_portrait, (0,0,0), (28, 40, 8, 2)) # Mouth
pygame.draw.line(elder_portrait, outline_color, (32, 42), (32, 48), 2) # Chin detail outline
pygame.draw.line(elder_portrait, (0,0,0), (32, 42), (32, 48), 1) # Chin detail

ep_font = pygame.font.Font(pygame.font.get_default_font(), 20) # Font, same size
ep_txt = ep_font.render("E", True, (255,255,255))
ep_txt_scaled = pygame.transform.scale(ep_txt, (int(ep_txt.get_width()*1.5), int(ep_txt.get_height()*1.5))) # Scale up text
elder_portrait.blit(ep_txt_scaled, ep_txt_scaled.get_rect(center=(32, 32 + 10))) # Shift text down

# Pixel noise for texture
elder_portrait = add_pixel_noise(elder_portrait, intensity=20)

save_asset(elder_portrait, "elder_portrait.png")


# --------------------- Detailed Level and Miscellaneous Assets ---------------------
level1_bg = pygame.Surface((800,600))
level1_bg.fill((25, 25, 25)) # Even darker background
grid_color = (40, 40, 40) # More subtle grid
for x in range(0, 801, 32):
    pygame.draw.line(level1_bg, grid_color, (x,0), (x,600))
for y in range(0, 601, 32):
    pygame.draw.line(level1_bg, grid_color, (0,y), (800,y))
# Pixel noise for background texture
level1_bg = add_pixel_noise(level1_bg, intensity=30)
save_asset(level1_bg, "level1_bg.png")


bg_layer1 = pygame.Surface((800,600))
# More textured background layer - varied tile pattern and shading - with outline
bg_tile_size = 20
bg_colors_base = [(35, 35, 65), (40, 40, 70), (45, 45, 75), (40, 40, 70)] # Base blue-grey tones
bg_colors_shade = [(30, 30, 60), (35, 35, 65), (40, 40, 70), (35, 35, 65)] # Shade tones
outline_color = (10, 10, 30) # Darker outline for tiles
for x in range(0, 800, bg_tile_size):
    for y in range(0, 600, bg_tile_size):
        color_base = random.choice(bg_colors_base)
        color_shade = random.choice(bg_colors_shade)
        pygame.draw.rect(bg_layer1, outline_color, (x, y, bg_tile_size, bg_tile_size), 1) # Tile outline
        pygame.draw.rect(bg_layer1, color_base, (x, y, bg_tile_size, bg_tile_size))
        if (x + y) % (bg_tile_size * 2) == 0: # Some tiles shaded
            pygame.draw.rect(bg_layer1, color_shade, (x, y, bg_tile_size, bg_tile_size))
# Pixel noise for texture
bg_layer1 = add_pixel_noise(bg_layer1, intensity=25)
save_asset(bg_layer1, "bg_layer1.png")


bg_layer2 = pygame.Surface((800,600))
# More detailed color gradient for bg_layer2 - subtle bands - with outline
outline_color = (10, 10, 30) # Darker outline for bands
for y in range(0, 600, 2): # Bands of 2 pixels
    t = y / 600
    color_base = (
        int(20*(1-t) + 30*t),
        int(20*(1-t) + 30*t),
        int(50*(1-t) + 60*t)
    )
    color_shade = (
        int(18*(1-t) + 28*t),
        int(18*(1-t) + 28*t),
        int(48*(1-t) + 58*t)
    )
    if (y // 2) % 2 == 0: # Alternate bands with shading
        pygame.draw.line(bg_layer2, outline_color, (0,y), (800,y), 1) # Band outline
        pygame.draw.line(bg_layer2, color_base, (0,y), (800,y), 2)
    else:
        pygame.draw.line(bg_layer2, outline_color, (0,y), (800,y), 1) # Band outline
        pygame.draw.line(bg_layer2, color_shade, (0,y), (800,y), 2)
# Pixel noise for texture
bg_layer2 = add_pixel_noise(bg_layer2, intensity=30)
save_asset(bg_layer2, "bg_layer2.png")


tileset = pygame.Surface((32*10, 32), pygame.SRCALPHA)
tile_colors_base = [
    (190,190,190), (170,170,170), (150,150,150),
    (130,130,130), (110,110,110), (90,90,90),
    (70,70,70), (50,50,50), (30,30,30), (10,10,10)
]
tile_colors_shade = [
    (170,170,170), (150,150,150), (130,130,130),
    (110,110,110), (90,90,90), (70,70,70),
    (50,50,50), (30,30,30), (10,10,10), (0,0,0)
]
outline_color = (20, 20, 20) # Tile outline color
for i in range(10):
    tile = pygame.Surface((32,32))
    tile.fill(tile_colors_base[i])
    if i % 2 == 0:
        pygame.draw.rect(tile, tile_colors_shade[i], (2,2,28,28)) # Shaded inner tile
        pygame.draw.rect(tile, outline_color, (1,1,30,30), 1) # Thinner tile border
        pygame.draw.line(tile, outline_color, (0,0), (32,32), 1) # Diagonal lines
        pygame.draw.line(tile, outline_color, (32,0), (0,32), 1)
    # Pixel noise for tile texture
    tile = add_pixel_noise(tile, intensity=20)
    tileset.blit(tile, (i*32, 0))
save_asset(tileset, "tileset.png")


tree = pygame.Surface((32,32), pygame.SRCALPHA)
# More detailed, pixel-art style tree - layered leaves and trunk texture - with outline
tree_trunk_color_base = (90, 60, 20)
tree_trunk_color_shade = (70, 40, 10)
tree_leaf_color_base = (20, 100, 20)
tree_leaf_color_shade = (10, 80, 10)
outline_color = (20, 20, 20) # Tree outline color

# Trunk - textured trunk with shading and outline
pygame.draw.rect(tree, outline_color, (12-1, 15-1, 8+2, 17+2), 1) # Trunk outline
pygame.draw.rect(tree, tree_trunk_color_base, (12, 15, 8, 17)) # Trunk base
pygame.draw.rect(tree, tree_trunk_color_shade, (12, 15, 2, 17)) # Trunk shading
pygame.draw.rect(tree, tree_trunk_color_shade, (18, 15, 2, 17)) # Trunk shading
pygame.draw.rect(tree, outline_color, (12, 15, 8, 17), 1) # Trunk border - already there, keep for emphasis

# Leaves - layered leaves with shading and outline
pygame.draw.circle(tree, outline_color, (16, 8), 17) # Leaf outline
pygame.draw.circle(tree, tree_leaf_color_base, (16, 8), 16) # Leaf base
pygame.draw.circle(tree, tree_leaf_color_shade, (18, 6), 14) # Leaf shading
pygame.draw.polygon(tree, tree_leaf_color_base, [(0, 15), (16, 0), (32, 15)]) # Leaf shape overlay
pygame.draw.polygon(tree, tree_leaf_color_shade, [(2, 15), (16, 2), (30, 15)]) # Leaf shape shading
pygame.draw.circle(tree, outline_color, (16, 8), 16, 1) # Leaf border - already there, keep for emphasis

# Pixel noise for texture
tree = add_pixel_noise(tree, intensity=10)

save_asset(tree, "tree.png")


rock = pygame.Surface((32,32), pygame.SRCALPHA)
# More detailed, pixel-art style rock - multi-layered, jagged edges - with outline
rock_color_base = (100, 100, 100)
rock_color_shade = (80, 80, 80)
rock_detail_color = (120, 120, 120)
outline_color = (20, 20, 20) # Rock outline color

# Rock shape - more complex polygon with outline
pygame.draw.polygon(rock, outline_color, [(4-1, 16), (16-1, 2), (28+1, 16), (28+1, 24), (16+1, 30), (4-1, 24)], 1) # Outline
pygame.draw.polygon(rock, rock_color_base, [(4, 16), (16, 2), (28, 16), (28, 24), (16, 30), (4, 24)]) # Base shape
pygame.draw.polygon(rock, rock_color_shade, [(4, 16), (16, 8), (28, 16), (28, 24), (16, 30), (4, 24)]) # Shading layer
pygame.draw.polygon(rock, rock_detail_color, [(8, 16), (16, 6), (24, 16), (24, 22), (16, 28), (8, 22)]) # Detail layer

# Edge details - jagged edges - border already acts as outline

# Pixel noise for texture
rock = add_pixel_noise(rock, intensity=10)

save_asset(rock, "rock.png")


intro_bg = pygame.Surface((800,600), pygame.SRCALPHA)
# More detailed intro background gradient - with noise and bands - with outline
outline_color = (10, 10, 30) # Darker outline for bands
for y in range(0, 600, 1): # Finer bands
    t = y / 600
    color_base = (
        int(10*(1-t) + 20*t),
        int(10*(1-t) + 20*t),
        int(30*(1-t) + 40*t)
    )
    color_shade = (
        int(8*(1-t) + 18*t),
        int(8*(1-t) + 18*t),
        int(28*(1-t) + 38*t)
    )
    if (y // 1) % 2 == 0: # Even finer bands with shading
        pygame.draw.line(intro_bg, outline_color, (0,y), (800,y), 1) # Band outline
        pygame.draw.line(intro_bg, color_base, (0,y), (800,y), 1)
    else:
        pygame.draw.line(intro_bg, outline_color, (0,y), (800,y), 1) # Band outline
        pygame.draw.line(intro_bg, color_shade, (0,y), (800,y), 1)
# Pixel noise for texture
intro_bg = add_pixel_noise(intro_bg, intensity=20)
save_asset(intro_bg, "intro_bg.png")


# --------------------- Detailed Sprite Sheet Assets ---------------------
# player_idle.png: 128x32 sprite sheet (4 frames of 32x32) - same size
player_idle = pygame.Surface((128,32), pygame.SRCALPHA)
for i in range(4):
    frame = pygame.Surface((32,32), pygame.SRCALPHA) # Frame, same size
    # Ukrainian soldier sprite (using function)
    frame.blit(generate_detailed_ukrainian_soldier(), (0,0))
    player_idle.blit(frame, (i*32, 0))
save_asset(player_idle, "player_idle.png")

# russian_invader.png: 128x32 sprite sheet (4 frames of 32x32) - same size
russian_invader = pygame.Surface((128,32), pygame.SRCALPHA)
for i in range(4):
    frame = pygame.Surface((32,32), pygame.SRCALPHA) # Frame, same size
    # Russian soldier sprite (using function)
    frame.blit(generate_detailed_russian_soldier(), (0,0))
    russian_invader.blit(frame, (i*32, 0))
save_asset(russian_invader, "russian_invader.png")


# --------------------- Detailed Building Assets ---------------------
fortress = pygame.Surface((160, 128), pygame.SRCALPHA) # Slightly taller fortress
# Fortress - even more detailed pixel art fortress - with outline
fortress_wall_color_base = (95, 95, 95)
fortress_wall_color_shade = (75, 75, 75)
fortress_detail_color = (85, 85, 85)
gate_color = (80, 60, 40)
gate_detail_color = (60, 40, 20)
outline_color = (20, 20, 20) # Fortress outline color

# Walls - layered walls with more detail and outline
pygame.draw.rect(fortress, outline_color, (8-1, 20-1, 144+2, 98+2), 1) # Wall outline
pygame.draw.rect(fortress, fortress_wall_color_base, (8, 20, 144, 98)) # Wall base
pygame.draw.polygon(fortress, fortress_wall_color_shade, [(8, 20), (80, 10), (152, 20), (152, 118), (8, 118)]) # Wall shading
# Battlements - more detailed battlements with outline
for x in range(20, 150, 20):
    pygame.draw.rect(fortress, outline_color, (x-1, 8-1, 12+2, 12+2), 1) # Battlement outline
    pygame.draw.rect(fortress, fortress_wall_color_base, (x, 8, 12, 12)) # Battlement base
    pygame.draw.rect(fortress, fortress_wall_color_shade, (x, 8, 3, 12)) # Battlement shading
    pygame.draw.rect(fortress, fortress_wall_color_shade, (x+9, 8, 3, 12)) # Battlement shading
# Gate - detailed gate with wood texture and outline
pygame.draw.rect(fortress, outline_color, (68-1, 100-1, 24+2, 28+2), 1) # Gate outline
pygame.draw.rect(fortress, gate_color, (68, 100, 24, 28)) # Gate base
pygame.draw.rect(fortress, gate_detail_color, (68, 100, 24, 8)) # Gate detail - top wood
pygame.draw.rect(fortress, gate_detail_color, (68, 112, 24, 8)) # Gate detail - middle wood
pygame.draw.rect(fortress, gate_detail_color, (68, 124, 24, 4)) # Gate detail - bottom wood
pygame.draw.rect(fortress, outline_color, (68, 100, 24, 28), 1) # Gate border - already there, keep for emphasis

# Wall details - stone blocks more defined
block_size = 8
for x in range(8, 152, block_size):
    pygame.draw.line(fortress, fortress_detail_color, (x, 20), (x, 118), 1)
for y in range(20 + block_size, 118, block_size):
    pygame.draw.line(fortress, fortress_detail_color, (8, y), (152, y), 1)
pygame.draw.rect(fortress, outline_color, (8, 20, 144, 98), 1) # Wall border - already there, keep for emphasis

# Pixel noise for texture
fortress = add_pixel_noise(fortress, intensity=20)

save_asset(fortress, "fortress.png")



village = pygame.Surface((128, 96), pygame.SRCALPHA) # Village, same size
# Village - even more detailed pixel art village houses - with outline
village_wall_color_base = (150, 130, 90)
village_wall_color_shade = (130, 110, 70)
village_roof_color_base = (110, 80, 50)
village_roof_color_shade = (90, 60, 30)
window_color = (180, 200, 220)
window_detail_color = (150, 170, 190)
door_color = (90, 70, 50)
door_detail_color = (70, 50, 30)
outline_color = (20, 20, 20) # Village outline color

# House 1 - more detailed house with outline
pygame.draw.rect(village, outline_color, (8-1, 28-1, 42+2, 42+2), 1) # House 1 outline
pygame.draw.rect(village, village_wall_color_base, (8, 28, 42, 42)) # House 1 wall base
pygame.draw.polygon(village, village_wall_color_shade, [(8, 28), (30, 23), (50, 28), (50, 70), (8, 70)]) # Wall shading
pygame.draw.polygon(village, outline_color, [(3-1, 28-1), (30, 3-1), (57+1, 28-1)], 1) # Roof outline
pygame.draw.polygon(village, village_roof_color_base, [(3, 28), (30, 3), (57, 28)]) # Roof base
pygame.draw.polygon(village, village_roof_color_shade, [(3, 28), (30, 8), (57, 28)]) # Roof shading
pygame.draw.rect(village, window_color, (18, 40, 12, 12)) # Window 1
pygame.draw.rect(village, window_detail_color, (18, 40, 3, 12)) # Window detail
pygame.draw.rect(village, door_color, (35, 50, 10, 20)) # Door 1
pygame.draw.rect(village, door_detail_color, (35, 50, 10, 5)) # Door detail

pygame.draw.rect(village, outline_color, (8, 28, 42, 42), 1) # House 1 border - already there, keep for emphasis

# House 2 - more detailed house with outline
pygame.draw.rect(village, outline_color, (68-1, 38-1, 42+2, 32+2), 1) # House 2 outline
pygame.draw.rect(village, village_wall_color_base, (68, 38, 42, 32)) # House 2 wall base
pygame.draw.polygon(village, village_wall_color_shade, [(68, 38), (90, 33), (110, 38), (110, 70), (68, 70)]) # Wall shading - NOTE: Y coord 70 is intentional to align with House 1
pygame.draw.polygon(village, outline_color, [(63-1, 38-1), (90, 13-1), (117+1, 38-1)], 1) # Roof outline
pygame.draw.polygon(village, village_roof_color_base, [(63, 38), (90, 13), (117, 38)]) # Roof base
pygame.draw.polygon(village, village_roof_color_shade, [(63, 38), (90, 18), (117, 38)]) # Roof shading
pygame.draw.rect(village, window_color, (78, 48, 12, 12)) # Window 2
pygame.draw.rect(village, window_detail_color, (78, 48, 3, 12)) # Window detail

pygame.draw.rect(village, outline_color, (68, 38, 42, 32), 1) # House 2 border - already there, keep for emphasis

# Pixel noise for texture
village = add_pixel_noise(village, intensity=20)

save_asset(village, "village.png")



def generate_detailed_poster(): # Modified propaganda poster - pro-Ukrainian
    poster = pygame.Surface((64, 96), pygame.SRCALPHA) # Poster, same size
    poster.fill((255,255,255))
    outline_color = (20, 20, 20) # Poster outline color
    pygame.draw.rect(poster, outline_color, (2-1,2-1,60+2,92+2), 1) # Border Outline
    pygame.draw.rect(poster, (0,0,0), (2,2,60,92), 1) # Border - already there, keep for emphasis

    # Flag colors - Ukrainian flag - with texture and outline
    flag_yellow_base = (255, 255, 100)
    flag_blue_base = (50, 100, 255)
    flag_blue_shade = (30, 80, 230)


    pygame.draw.rect(poster, outline_color, (4-1, 8-1, 56+2, 40+2), 1) # Yellow stripe outline - increased height
    pygame.draw.rect(poster, flag_yellow_base, (4, 8, 56, 40)) # Yellow stripe base - increased height
    pygame.draw.rect(poster, outline_color, (4-1, 48-1, 56+2, 40+2), 1) # Blue stripe outline - increased height
    pygame.draw.rect(poster, flag_blue_base, (4, 48, 56, 40)) # Blue stripe base - increased height
    pygame.draw.rect(poster, flag_blue_shade, (4, 48, 56, 10)) # Blue stripe shading - adjusted shading


    # Text - "Stand With Ukraine" - at the bottom, more pixel art style, more defined
    p_font = pygame.font.Font(pygame.font.get_default_font(), 8) # Font, same size
    p_text = p_font.render("STAND WITH", True, (0,0,0)) # "STAND WITH" in black
    p_text2 = p_font.render("UKRAINE", True, (flag_blue_base)) # "UKRAINE" in blue - base blue color
    poster.blit(p_text, p_text.get_rect(center=(32, 77 + 12))) # Shift text to bottom - adjusted shift
    poster.blit(p_text2, p_text2.get_rect(center=(32, 87 + 12))) # Shift text to bottom - adjusted shift

    # Pixel noise for texture
    poster = add_pixel_noise(poster, intensity=15)

    return poster

poster = generate_detailed_poster()
save_asset(poster, "propaganda_poster.png")



# --------------------- Detailed Drone Asset ---------------------
drone = pygame.Surface((32,32), pygame.SRCALPHA) # Drone, same size
drone_body_color_base = (110, 110, 130) # Grey-blue drone color, darker
drone_body_color_shade = (90, 90, 110)
drone_propeller_color = (60, 60, 80) # Darker propellers
drone_detail_color = (130, 130, 150) # Lighter detail color
outline_color = (20, 20, 20) # Drone outline color

# Drone body - more aerodynamic shape with layered shading and outline
pygame.draw.ellipse(drone, outline_color, (4-1, 4-1, 24+2, 24+2), 1) # Body outline
pygame.draw.ellipse(drone, drone_body_color_base, (4, 4, 24, 24)) # Body base ellipse
pygame.draw.ellipse(drone, drone_body_color_shade, (4, 4, 12, 24)) # Body side shading
pygame.draw.rect(drone, drone_body_color_base, (4, 4, 24, 10)) # Body top rect
pygame.draw.polygon(drone, drone_body_color_shade, [(4, 4), (16, 2), (28, 4), (28, 14), (4, 14)]) # Body top shading


# Propellers - more detailed propellers with blades and outline
propeller_size = 5
for angle_offset in range(0, 360, 90): # Rotated propellers
    angle_rad = math.radians(angle_offset)
    center_x = 16 + int(12 * math.cos(angle_rad))
    center_y = 16 + int(12 * math.sin(angle_rad))
    pygame.draw.rect(drone, outline_color, (center_x - propeller_size//2 -1, center_y - propeller_size//2-1, propeller_size+2, propeller_size+2), 1) # Prop base outline
    pygame.draw.rect(drone, drone_propeller_color, (center_x - propeller_size//2, center_y - propeller_size//2, propeller_size, propeller_size), border_radius=1) # Prop base
    pygame.draw.rect(drone, drone_detail_color, (center_x - 1, center_y - propeller_size//2 - 2, 2, 4)) # Prop blade 1
    pygame.draw.rect(drone, drone_detail_color, (center_x - propeller_size//2 - 2, center_y - 1, 4, 2)) # Prop blade 2

# Camera - front camera detail with outline
pygame.draw.circle(drone, outline_color, (16, 8), 4) # Camera lens outline
pygame.draw.circle(drone, drone_detail_color, (16, 8), 3) # Camera lens
pygame.draw.circle(drone, outline_color, (16, 8), 3, 1) # Camera border - already there, keep for emphasis

pygame.draw.rect(drone, outline_color, (4, 4, 24, 24), 1, border_radius=12) # Body border - already there, keep for emphasis

d_font = pygame.font.Font(pygame.font.get_default_font(), 8) # Font, same size
d_text = d_font.render("D", True, (255,255,255))
d_text_scaled = pygame.transform.scale(d_text, (int(d_text.get_width()*1.2), int(d_text.get_height()*1.2))) # Scale up text
drone.blit(d_text_scaled, d_text_scaled.get_rect(center=(16,16+2))) # Shift text down

# Pixel noise for texture
drone = add_pixel_noise(drone, intensity=10)


save_asset(drone, "drone.png")



# --------------------- Detailed Vehicle Assets ---------------------
def generate_detailed_tank_t72(): # Even more detailed tank
    surf = pygame.Surface((64, 32), pygame.SRCALPHA) # Tank sprite size, same
    tank_color_base = (80, 85, 70) # Tank green base
    tank_color_shade = (55, 60, 45) # Tank green shade
    tank_track_color = (45, 45, 45) # Track color, darker
    tank_track_detail = (60, 60, 60) # Track detail, lighter
    black = (0, 0, 0)
    outline_color = (20, 20, 20) # Tank outline color

    # Tracks - more detailed tracks with individual treads and outline
    pygame.draw.rect(surf, outline_color, (0-1, 20-1, 64+2, 12+2), 1) # Track outline
    pygame.draw.rect(surf, tank_track_color, (0, 20, 64, 12)) # Track base
    for x in range(1, 63, 2): # Individual treads
        pygame.draw.rect(surf, tank_track_detail, (x, 20, 1, 12))
    for x in range(0, 64, 8): # Track details - horizontal lines
        pygame.draw.rect(surf, black, (x, 20, 1, 12)) # Vertical track lines - changed to black for contrast
        pygame.draw.rect(surf, black, (x+2, 20, 1, 12)) # Vertical track lines
        pygame.draw.rect(surf, black, (x+4, 20, 1, 12)) # Vertical track lines
        pygame.draw.rect(surf, black, (x+6, 20, 1, 12)) # Vertical track lines

    # Body - detailed body with angles and outline
    pygame.draw.polygon(surf, outline_color, [(4-1, 4-1), (60+1, 4-1), (64+1, 12), (0-1, 12)], 1) # Body outline
    pygame.draw.polygon(surf, tank_color_base, [(4, 4), (60, 4), (64, 12), (0, 12)]) # Main body
    pygame.draw.polygon(surf, tank_color_shade, [(4, 4), (32, 2), (60, 4), (60, 12), (4, 12)]) # Body shading
    pygame.draw.rect(surf, tank_color_base, (6, 12, 52, 6)) # Lower body detail
    pygame.draw.rect(surf, tank_color_shade, (6, 12, 52, 2)) # Lower body shading

    # Turret - detailed turret with gun and outline
    pygame.draw.circle(surf, outline_color, (32, 4), 13) # Turret base outline
    pygame.draw.circle(surf, tank_color_base, (32, 4), 12) # Turret base
    pygame.draw.circle(surf, tank_color_shade, (34, 6), 10) # Turret shading
    pygame.draw.rect(surf, outline_color, (32-10-1, 4-2-1, 20+2, 4+2), 1) # Gun outline
    pygame.draw.rect(surf, tank_track_color, (32-10, 4-2, 20, 4)) # Gun barrel

    # Pixel noise for texture
    surf = add_pixel_noise(surf, intensity=10)

    return surf

tank_t72 = generate_detailed_tank_t72()
save_asset(tank_t72, "tank_t72.png")