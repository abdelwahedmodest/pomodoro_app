from PIL import Image

# Open the JPG image
img = Image.open('icon_pomodoro.jpg')

# Convert and save as ICO
img.save('icon_pomodoro.ico', format='ICO')
