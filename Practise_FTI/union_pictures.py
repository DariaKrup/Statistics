import os
import PIL
from PIL import Image
from PIL import ImageDraw, ImageFont
import numpy as np

os.chdir("C:\\Users\\Daria\\Documents\\Practise_FTI\\code\\fragment_w_graph")
image_folder = '.'
images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png")]
images = sorted(images, key = os.path.getmtime)
imgs = [PIL.Image.open(i) for i in images]
quan = len(imgs)
font = ImageFont.truetype("arial.ttf", 40)
for i in range(quan):
    draw_text = ImageDraw.Draw(imgs[i])
    if i != quan - 1:
        text = 'Layer 7, cell = ' + str(i + 1)
    else:
        text = 'Full 7 layer'
    draw_text.text((100, 100), text, fill=('#1C0606'), font=font)
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
step = 3
parts = len(imgs) // step
ind_start = 0
for area in range(1, parts + 1):
    imgs_comb = np.vstack((np.asarray(im.resize(min_shape)) for im in imgs[ind_start:ind_start + step]))
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    image_name = 'area' + str(area) + '.png'
    imgs_comb.save(image_name)
    ind_start += step
    #area += 1
area_img = ['area1.png', 'area2.png', 'area3.png', 'area4.png', 'area5.png', 'area6.png', 'area7.png', 'area8.png', 'area9.png']
area_imgs = [PIL.Image.open(i) for i in area_img]
min_shape = sorted([(np.sum(i.size), i.size) for i in area_imgs])[0][1]
imgs_comb_h1 = np.hstack((np.asarray(i.resize(min_shape)) for i in area_imgs[0:5]))
imgs_comb_h2 = np.hstack((np.asarray(i.resize(min_shape)) for i in area_imgs[5:9]))
imgs_comb_h1 = PIL.Image.fromarray(imgs_comb_h1)
imgs_comb_h2 = PIL.Image.fromarray(imgs_comb_h2)
imgs_comb_h1.save('cells1.png')
imgs_comb_h2.save('cells2.png')
imgs_fin = ['cells1.png', 'cells2.png']
imgs_fin = [PIL.Image.open(i) for i in imgs_fin]
min_shape = sorted([(np.sum(i.size), i.size) for i in imgs_fin])[0][1]
imgs_comb_fin = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs_fin))
imgs_comb_fin = PIL.Image.fromarray(imgs_comb_fin)
imgs_comb_fin.save('All cells.png')