import glob
import cv2 as c
import time
start=time.time()
def kernal(image, prob):
 op = c.GaussianBlur(image, (51, 51), 0)
 return op
p = "true1.jpg"
for file in glob.glob(p):
 print(file)
 img = c.imread(file,1)
 out=kernal(img,.01)
 c.imshow("blurred",out)
 c.imwrite("C:\\Users\\hp\\OneDrive\\Desktop\\mini project\\demo\\kernal_true1.jpg",out)
end=time.time()
print("Execution time:",end-start)
