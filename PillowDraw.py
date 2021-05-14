from PIL import Image as Im, ImageDraw as Imd, ImageFont as Imf
image = Im.new("RGB", (512, 512), (0, 0, 0))
drawing = Imd.Draw(image)

font = Imf.truetype('/Windows/Fonts/Arial.ttf', 12)
drawing.multiline_text((32, 256), "Hi Caitlin! I made this with python! You're so cute and I'm going to date you so hard!", fill=(50, 111, 215), font=font)
image.save('PillowDraw/PillowDraw.png', quality=100)