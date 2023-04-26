from PIL import Image
import strings as ss
import os


def start(idx):
    if not os.path.exists(str(idx)):
        os.mkdir(str(idx))
    empty = Image.open("photo/empty{}.png".format(ss.theme))
    temp = empty.copy()
    temp.save('{}/temp.png'.format(idx))


def paste(lx, ly, orientation, length, idx):
    if orientation == "v":
        ry = ly + length
        rx = lx + 1
    else:
        rx = lx + length
        ry = ly + 1
    full = Image.open("photo/full{}.png".format(ss.theme))
    temp = Image.open("{}/temp.png".format(idx))
    x, y = ss.px[ss.theme - 1]
    temp.paste(full.crop((x * lx, y * ly, x * rx, y * ry)), (x * lx, y * ly))
    temp.save('{}/temp.png'.format(idx))
    full.close()
    temp.close()
