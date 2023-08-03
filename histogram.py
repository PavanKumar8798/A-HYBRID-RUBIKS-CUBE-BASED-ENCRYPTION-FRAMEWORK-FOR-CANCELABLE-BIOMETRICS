import cv2 as c
from matplotlib import pyplot as pt
image = c.imread("cfb_9.jpg")
pt.hist(image.ravel(),256,[0,256])
pt.show()
