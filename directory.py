import os
from treelib import Tree
from PIL import Image, ImageDraw, ImageFont
import textwrap

def build_tree(tree, parent, path):
    for item in sorted(os.listdir(path)):
        full_path = os.path.join(path, item)
        if item == ".venv":
            continue
        tree.create_node(item, full_path, parent=parent)
        if os.path.isdir(full_path):
            build_tree(tree, full_path, full_path)

def generate_tree_text(root_path):
    tree = Tree()
    tree.create_node(os.path.basename(root_path), root_path)
    build_tree(tree, root_path, root_path)
    return tree.show(stdout=False)  

def save_tree_as_image(tree_text, output_file):
    """Converts the tree text into an image"""
    font_size = 16
    lines = tree_text.split("\n")
    
    max_width = max(len(line) for line in lines) * (font_size // 2)
    height = font_size * (len(lines) + 2)  
    
    img = Image.new("RGB", (max_width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)  
    except IOError:
        font = ImageFont.load_default()  

    for i, line in enumerate(lines):
        wrapped_lines = textwrap.wrap(line, width=80) 
        for j, wrapped_line in enumerate(wrapped_lines):
            draw.text((10, (i + j) * font_size), wrapped_line, fill="black", font=font)
    
    img.save(output_file, format="PNG")  
    print(f"✅ Directory tree saved as {output_file}")

script_dir = os.path.dirname(os.path.abspath(__file__)) 

if not os.path.exists(script_dir):
    print(f"❌ Error: Directory '{script_dir}' not found.")
    exit(1)

output_file = os.path.join(script_dir, "directory_tree.png") 

tree_text = generate_tree_text(script_dir)
save_tree_as_image(tree_text, output_file)