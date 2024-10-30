import os
import argparse

from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import math
import numpy as np

home_dir = os.path.expanduser('~')

#ch_file = os.path.join(home_dir, "Documents", "python", "64ch.ced")
ch_file = "Standard-10-20-Cap81.ced"

def circle(x, y, radius):
    val = (x-radius, y-radius, x+radius, y+radius)
    return val

def circle_ycoff(x, y, radius, y_coff):
    val = (x-radius, (y-radius)*y_coff, x+radius, (y+radius)*y_coff)
    return val

class convert():
    def __init__(self, size):
        self.size = size
        self.offset_x = int(size[0]/2)
        self.offset_y = int(size[1]/2)

    def zeroing(self, pos):
        val = (pos[0] + self.offset_x, pos[1] + self.offset_y, pos[2] + self.offset_x, pos[3] + self.offset_y)
        
        return val

    def zeroing_2d(self, pos):
        val = (pos[0] + self.offset_x, pos[1] + self.offset_y)
        return val

def draw_nose(draw, width, length, y_offset, img_size):
    p1 = [0,0]
    p2 = [-width/2, length]
    p3 = [width/2, length]
    p = [p1, p2, p3]
    
    for idx, _p in enumerate(p):
        p[idx] = (p[idx][0]+(img_size[0]/2), p[idx][1]+(img_size[1]/2) + y_offset)
    
    draw.polygon(p, fill=(255, 255, 255), outline=(0, 0, 0), width = 10)

def cap_ch(ch: str):
    import copy
    _ch = copy.deepcopy(ch).lower()
    if _ch.startswith("fp"):
        _ch = _ch.capitalize()
    elif _ch.startswith("af"):
        _ch = _ch.upper()
        if _ch == "AFZ":
            _ch = "AFz"
    elif _ch.startswith("fc"):
        _ch = _ch.upper()
        if _ch == "FCZ":
            _ch = "FCz"
    elif _ch.startswith("ft"):
        _ch = _ch.upper()
    elif _ch.startswith("f"):
        _ch = _ch.capitalize()
    elif _ch.startswith("t"):
        _ch = _ch.upper()
    elif _ch.startswith("cp"):
        _ch = _ch.upper()
        if _ch == "CPZ":
            _ch = "CPz"
    elif _ch.startswith("c"):
        _ch = _ch.capitalize()
    elif _ch.startswith("po"):
        _ch = _ch.upper()
        if _ch == "POZ":
            _ch = "POz"
    elif _ch.startswith("p"):
        _ch = _ch.capitalize()
    elif _ch.startswith("o"):
        _ch = _ch.upper()
        if _ch == "OZ":
            _ch = "Oz"
    return _ch

#with open(os.path.join(home_dir, "Documents", "python", "64ch.ced")) as f:
#    print(f.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ch", type = str, nargs = '*', default = None)
    parser.add_argument("--vhdr", type = str, default = None)
    parser.add_argument("--eog", type = str, default = None, nargs = '*')
    args = parser.parse_args()
    
    ch = None
    if args.ch is not None:
        ch = args.ch
    elif args.vhdr is not None:
        import mne
        if args.eog is not None:
            eog = args.eog
        else:
            eog = ('HEOGL', 'HEOGR', 'VEOGb')
        raw = mne.io.read_raw_brainvision(args.vhdr, eog = eog)
        print("channels: %s"%str(raw.ch_names))
        print("channels after picking eeg: %s"%str(raw.pick(picks = 'eeg').ch_names))
        ch = raw.pick(picks='eeg').ch_names

    df = pd.read_csv(ch_file, sep="\t")
    print(df)

    size = (6000, 6000)
    coff = size[0]/1.5

    img = Image.new('RGB', size, (255,255,255))
    cvt = convert(size = size)

    draw = ImageDraw.Draw(img)

    theta = df["theta"].tolist()
    rads = df["radius"].tolist()
    labels = df["labels"].tolist()
    
    labels = [m.lower() for m in labels]
    
    print(labels)
    idx = []
    for _ch in ch:
        if _ch.lower() in labels:
            _idx = labels.index(_ch.lower())
            idx.append(_idx)
        else:
            raise RuntimeError("channel '%s' is not found in ced file"%_ch.lower())
    
    # pick channels selected
    labels = [labels[m] for m in idx]
    theta = [theta[m] for m in idx]
    rads = [rads[m] for m in idx]

    head_rad = max(rads)

    draw_nose(draw = draw, width = 1500, length = 1000, y_offset = -2800, img_size=size)
    draw.ellipse(cvt.zeroing(circle_ycoff(x = 0, y = 0, radius = coff * head_rad, y_coff=0.95)), fill = (255, 255, 255), outline = (0,0,0), width = 10)

    #font = ImageFont.truetype(os.path.join(home_dir, "Documents", "python", 'Arial.ttf'), 115)
    font = ImageFont.truetype("Arial.ttf", 115)

    for m in range(0, 64):
        x = math.sin(math.radians(theta[m])) * rads[m] * coff
        y = -1 * math.cos(math.radians(theta[m])) * rads[m] * coff
        draw.ellipse(cvt.zeroing(circle(x = x, y = y, radius = 150)), fill=(255, 0, 0), outline=(255, 255, 255))
        draw.text(cvt.zeroing_2d((x, y)), text = cap_ch(labels[m]), anchor = 'mm', font = font)

    img.save(os.path.join(home_dir, "Documents", "python", 'montage.tiff'))