import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

filename = "C:/Users/timro/source/ThesisRepos/VoxelCubeTest/Symbols/5x5_pixel.ttf"
# font = ImageFont.truetype("Arial-Bold.ttf",14)
font = ImageFont.truetype(filename,8)
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
for letter in letters:
    img=Image.new("1", (5,5),(1))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0),letter,(0),font=font)
    draw = ImageDraw.Draw(img)
    img.save(f"Symbols/{letter}.png")