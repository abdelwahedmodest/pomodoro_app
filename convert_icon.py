from PIL import Image
import os

def convert_to_ico(png_path, ico_path):
    # Open the PNG image
    with Image.open(png_path) as img:
        # Convert to RGBA if not already
        img = img.convert('RGBA')
        # Create ICO file
        img.save(ico_path, format='ICO')

if __name__ == '__main__':
    # Convert PNG to ICO
    png_file = 'circular_logo_pomodoro.png'
    ico_file = 'pomodoro.ico'
    
    if os.path.exists(png_file):
        convert_to_ico(png_file, ico_file)
        print(f"Successfully converted {png_file} to {ico_file}")
    else:
        print(f"Error: {png_file} not found")
