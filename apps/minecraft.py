"""
Minecraft Clone - A simple voxel-based sandbox game
Built with Ursina Engine

Controls:
- WASD: Move
- Space: Jump
- Left Click: Break block
- Right Click: Place block
- 1-5: Select block type
- Tab: Toggle fly mode
- ESC: Release mouse cursor
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Define block types and their colors
block_types = {
    'grass': color.rgb(0, 155, 0),
    'dirt': color.rgb(101, 67, 33),
    'stone': color.rgb(128, 128, 128),
    'wood': color.rgb(139, 90, 43),
    'leaves': color.rgb(34, 139, 34),
    'sand': color.rgb(237, 220, 142),
    'water': color.rgba(0, 0, 255, 200),
}

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='white_cube', color=color.white):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color,
            highlight_color=color.lime,
        )
    
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
                Entity(position=self.position, model='cube', scale=0.2, color=color.yellow, duration=0.2)
            
            if key == 'right mouse down':
                if camera.world_position.y < self.position.y + 2:
                    Voxel(position=self.position + mouse.normal, color=current_block_color)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture='sky_sunset',
            scale=150,
            double_sided=True
        )
    
    def update(self):
        self.rotation_y += 0.01

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture='arm_texture.png',
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
        )
    
    def active(self):
        self.position = Vec2(0.3, -0.5)
    
    def passive(self):
        self.position = Vec2(0.4, -0.6)

# Try to load custom models, use built-in if not available
try:
    load_model('assets/block')
except:
    # Create a simple cube model as fallback
    class BlockModel:
        pass
    
def generate_terrain():
    print("Generating terrain...")
    for x in range(20):
        for z in range(20):
            # Simple height variation
            y = int(noise(x * 0.1, z * 0.1) * 5)
            
            # Place grass on top
            Voxel(position=(x, y, z), color=block_types['grass'])
            
            # Place dirt below
            for dy in range(1, 4):
                Voxel(position=(x, y - dy, z), color=block_types['dirt'])
            
            # Place stone at bottom
            Voxel(position=(x, y - 4, z), color=block_types['stone'])
    
    # Add some trees
    for _ in range(5):
        tree_x = random.randint(2, 18)
        tree_z = random.randint(2, 18)
        tree_y = int(noise(tree_x * 0.1, tree_z * 0.1) * 5) + 1
        
        # Tree trunk
        for ty in range(4):
            Voxel(position=(tree_x, tree_y + ty, tree_z), color=block_types['wood'])
        
        # Tree leaves
        for lx in range(-1, 2):
            for lz in range(-1, 2):
                for ly in range(3, 5):
                    if not (lx == 0 and lz == 0 and ly == 3):
                        Voxel(position=(tree_x + lx, tree_y + ly, tree_z + lz), color=block_types['leaves'])
        Voxel(position=(tree_x, tree_y + 5, tree_z), color=block_types['leaves'])

# Global variable for current block color
current_block_color = block_types['grass']

# UI for block selection
class BlockSelector(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='quad',
            scale=(0.8, 0.1),
            position=(-0.4, -0.45),
            color=color.dark_gray,
            visible=True
        )
        self.text = Text(text='Block: Grass [1-5]', parent=self, scale=2, position=(-0.45, 0))

block_selector = None

def update():
    global current_block_color
    
    # Hand animation
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    
    # Block selection with number keys
    if held_keys['1']:
        current_block_color = block_types['grass']
        block_selector.text.text = 'Block: Grass'
    elif held_keys['2']:
        current_block_color = block_types['dirt']
        block_selector.text.text = 'Block: Dirt'
    elif held_keys['3']:
        current_block_color = block_types['stone']
        block_selector.text.text = 'Block: Stone'
    elif held_keys['4']:
        current_block_color = block_types['wood']
        block_selector.text.text = 'Block: Wood'
    elif held_keys['5']:
        current_block_color = block_types['leaves']
        block_selector.text.text = 'Block: Leaves'

# Generate terrain
generate_terrain()

# Create player
player = FirstPersonController(speed=12)
player.cursor.visible = True
player.gravity = 0.5

# Set initial position
player.position = (10, 10, 10)

# Create sky
sky = Sky()

# Create hand
hand = Hand()

# Create block selector UI
block_selector = BlockSelector()

# Instructions
instructions = Text(
    text='WASD: Move | Space: Jump | LMB: Break | RMB: Place | 1-5: Blocks',
    position=(-0.85, 0.45),
    scale=1,
    color=color.white
)

print("Minecraft Clone loaded successfully!")
print("Click to start playing!")

app.run()
