# Karuta Frame Game Match Maker
# Made By zach1502#4621

# Do NOT use any part of this code without permission. Feel free to ask me on Discord for permission.
# Special thanks to the libraries used.

from __future__ import print_function
from PIL import Image, ImageDraw
import numpy as np
import os

def find_color(im):
    im = im.crop((0, 0, im.size[0], 50))
    color = im.getpixel((im.size[0]/2, im.size[1]/2))

    # saturate the color
    dark_multiplier = 1/800
    dark_factor = (int((dark_multiplier)*(color[0]*color[0] - 65025)), int((dark_multiplier)*(color[1]*color[1] - 65025)), int((dark_multiplier)*(color[2]*color[2] - 65025)))
    color = (color[0] + dark_factor[0], color[1] + dark_factor[1], color[2] + dark_factor[2], 255)
    return color


# find all images in the directory and put it into a list
def find_images(directory):
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                images.append(os.path.join(root, file))
    return images

def scramble_images(images):
    np.random.shuffle(images)
    return images

def gradient(color):
    img = Image.new("RGBA", (1920,1080), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    r,g,b,a = color
    dr = (r)/960.
    dg = (g)/960.
    db = (b)/960.
    da = (a)/960.

    for i in range(1920):
        r,g,b,a = r+dr, g+dg, b+db, a-da
        draw.line((i,0,i,1920), fill=(int(r),int(g),int(b),int(a)))


    return img


def create_match(images):
    # get length of list
    length = len(images)
    scramble_images(images)

    versus_img = Image.open("versus.png")
    versus_offset = (0, 0)
    bg_dim = (1920, 1080)

    for i in range(0, (int)(length), 2):
        # white background
        background = Image.new('RGBA', bg_dim, (255, 255, 255, 255))

        # open image
        left_img = Image.open(images[i])
        right_img = Image.open(images[i+1])

        left_fade_img = gradient(find_color(left_img))
        right_fade_img = gradient(find_color(right_img)).rotate(180)

        background.paste(left_fade_img, (0, 0), left_fade_img)
        background.paste(right_fade_img, (1920 - right_fade_img.size[0] , 0), right_fade_img)

        limg_w, limg_h = left_img.size
        rimg_w, rimg_h = right_img.size

        # scale the images by 1.95x
        scale_factor = 1.95

        left_img = left_img.resize((int(limg_w * scale_factor), int(limg_h * scale_factor)))
        right_img = right_img.resize((int(rimg_w * scale_factor), int(rimg_h * scale_factor)))

        # paste the images into the background
        right_offset = (bg_dim[0] - rimg_w*2 - 150, (bg_dim[1]//2) - rimg_h)
        left_offset = (150 , (bg_dim[1]//2) - limg_h)

        background.paste(left_img, left_offset, left_img)
        background.paste(right_img, right_offset, right_img)
        background.paste(versus_img, versus_offset, versus_img)

        # save the image
        background.save("matches/match " + str(i)+ " vs " + str(i+1) + ".png")

def main():
    images = find_images("images")
    create_match(images)

if __name__ == "__main__":
    main()






