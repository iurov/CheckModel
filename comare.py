from collections import defaultdict
from PIL import Image
import cv2
import tensorflow as tf
import numpy as np
from scipy import signal
from scipy.ndimage.filters import convolve
from skimage.measure import compare_ssim as ssim

def _get_variance(color_count: dict, average: float) -> float:
    variance = 0.0
    for pixel in color_count:
        a = pixel - average
        variance += color_count[pixel] * a * a
    return variance


def ssim_sum(image_0, image_1, tile_size, pixel_len, width, height, c_1, c_2):
    channels = range(len(image_0.mode))
    ssim_sum = 0.0
    back_count = 0
    joj=0

    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):

            flag = 0
            box = (x, y, x + 7, y + 7)
            tile_0 = image_0.crop(box)
            tile_1 = image_1.crop(box)
            r1 = tile_0.getdata(band=0)[0]
            g1 = tile_0.getdata(band=1)[0]
            b1 = tile_0.getdata(band=2)[0]
            r2 = tile_1.getdata(band=0)[0]
            g2 = tile_1.getdata(band=1)[0]
            b2 = tile_1.getdata(band=2)[0]
            if ((r1==r2) and (g1==g2) and (b2==b2) and (r1 == 236) and (g1==0) and (b1==255)):
                back_count += 3 * tile_size * tile_size
                flag = 1
            if flag == 0:
                for i in channels:
                    pixel0, pixel1 = tile_0.getdata(band=i), tile_1.getdata(band=i)
                    color_count_0 = defaultdict(int)
                    color_count_1 = defaultdict(int)
                    covariance = 0.0

                    for i1, i2 in zip(pixel0, pixel1):
                        color_count_0[i1] += 1
                        color_count_1[i2] += 1
                        covariance += i1 * i2

                    pixel_sum_0 = sum(pixel0)
                    pixel_sum_1 = sum(pixel1)
                    average_0 = pixel_sum_0 / pixel_len
                    average_1 = pixel_sum_1 / pixel_len

                    covariance = (covariance - pixel_sum_0 * pixel_sum_1 / pixel_len) / pixel_len
                    variance_0_1  = _get_variance(color_count_0, average_0)
                    variance_0_1 += _get_variance(color_count_1, average_1)
                    variance_0_1 /= pixel_len

                    ssim_sum += (2.0 * average_0 * average_1 + c_1) * (2.0 * covariance + c_2) / (
                            average_0 * average_0 + average_1 * average_1 + c_1) / (variance_0_1 + c_2)
                
    return ssim_sum, back_count

def compare_ssim(image_0, image_1, tile_size: int = 7, GPU: bool = False) -> float:
    dynamic_range = 255
    c_1 = (dynamic_range * 0.01) ** 2
    c_2 = (dynamic_range * 0.03) ** 2
    pixel_len = tile_size * tile_size
    width, height = image_0.size
    width = width // tile_size * tile_size
    height = height // tile_size * tile_size

    if image_0.size != image_1.size:
        raise AttributeError('The images do not have the same resolution')
    if image_0.mode != image_1.mode:
        raise AttributeError('The images have different color channels')
    if width < tile_size or height < tile_size:
        raise AttributeError('The images are smaller than the window_size')
    if tile_size < 1:
        raise AttributeError('The tile_size must be 1 or greater')

    get_ssim_sum, back = ssim_sum(image_0, image_1, tile_size, pixel_len, width, height, c_1, c_2)
    return get_ssim_sum * pixel_len / (
            len(image_0.mode) * (width) * (height)-back)

def compare_ms_ssim(im1, im2, levels=3):
    s = []
    ss = 0
    for i in range(levels):
        if i != 0:
            k = 1
            for j in range(i):
                k *= 2
            size = (im1.size[0]/k, im1.size[1]/k)
            im1.thumbnail(size, Image.ANTIALIAS)
            im2.thumbnail(size, Image.ANTIALIAS)
            s.append(compare_ssim(im1, im2))
    for i in s:
        ss += i
    return ss/len(s)

def floodFill(x,y, d,e,f, g,h,i, image):
    toFill = set()
    toFill.add((x,y))
    while not len(toFill)==0:
        (x,y) = toFill.pop()
        a,b,c = image.getpixel((x,y))
        if not (a,b,c) == (0, 0, 0):
            continue
        image.putpixel((x,y), (g,h,i))
        toFill.add((x-1,y))
        toFill.add((x+1,y))
        toFill.add((x,y-1))
        toFill.add((x,y+1))


def ch(file):
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = np.zeros_like(img)
    img2[:,:,0] = gray
    img2[:,:,1] = gray
    img2[:,:,2] = gray
    cv2.circle(img2, (10,10), 5, (255,255,0))
    cv2.imwrite(file, img)
    flood = Image.open(file)
    floodFill (2,2, 0,0,0,236, 0, 255,flood)
    flood.save(file)

def rez(param="SSIMM"):
    ev = 0
    i = 0
    while i < 10:
        if param == "SSIMM":
            f1 = Image.open("renders1/pose_"+str(i)+".png")
            f2 = Image.open("renders/pose_"+str(i)+".png")
            ev = ev + compare_ssim(f1, f2)
        else:
            if param == "MS-SSIM":
                f1 = Image.open("renders1/pose_"+str(i)+".png")
                f2 = Image.open("renders/pose_"+str(i)+".png")
                ev = ev + compare_ms_ssim(f1, f2)
            else:
                if param == "G-SSIM":
                    scale = 1
                    delta = 0
                    ddepth = cv2.CV_16S
                    src1 = cv2.imread("renders1/pose_"+str(i)+".png", cv2.IMREAD_COLOR)
                    src2 = cv2.imread("renders/pose_"+str(i)+".png", cv2.IMREAD_COLOR)    
                    src1 = cv2.GaussianBlur(src1, (3, 3), 0)
                    src2 = cv2.GaussianBlur(src2, (3, 3), 0)     
                    gray1 = cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)
                    gray2 = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY)      
                    grad_x1 = cv2.Sobel(gray1, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
                    grad_y1 = cv2.Sobel(gray1, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
                    grad_x2 = cv2.Sobel(gray2, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
                    grad_y2 = cv2.Sobel(gray2, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)       
                    abs_grad_x1 = cv2.convertScaleAbs(grad_x1)
                    abs_grad_y1 = cv2.convertScaleAbs(grad_y1)
                    abs_grad_x2 = cv2.convertScaleAbs(grad_x2)
                    abs_grad_y2 = cv2.convertScaleAbs(grad_y2)    
                    grad1 = cv2.addWeighted(abs_grad_x1, 0.5, abs_grad_y1, 0.5, 0)
                    grad2 = cv2.addWeighted(abs_grad_x2, 0.5, abs_grad_y2, 0.5, 0)    
                    cv2.imwrite('grad1.png', grad1)
                    cv2.imwrite('grad2.png', grad2)
                    ch("grad1.png")
                    ch("grad2.png")
                    f1 = Image.open("grad1.png")
                    f2 = Image.open("grad2.png")
                    ev = ev + compare_ssim(f1, f2)
                else:
                    if param == "SSIM":
                        frst = cv2.imread("renders1/pose_"+str(i)+".png")
                        hm = cv2.imread("renders/pose_"+str(i)+".png")
                        ev += ssim(frst, hm, multichannel=True)
        i += 1

    ev = int(ev*10)
    # print(ev)
    if param == "SSIMM":
        my_file = open("statm.txt", "a")
    if param == "MS-SSIM":
        my_file = open("statms.txt", "a")
    if param == "G-SIMM":
        my_file = open("statg.txt", "a")
    if param == "SSIM":
        my_file = open("stat.txt", "a")
    my_file.write(str(ev)+"\n")
    my_file.close()
