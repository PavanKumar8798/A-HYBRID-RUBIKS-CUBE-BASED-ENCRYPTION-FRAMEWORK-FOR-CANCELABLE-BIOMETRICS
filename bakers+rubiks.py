import sys as s
import cv2 as c
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import *
#import Crypto.Random.get_random_bytes as get_random_byte
import PIL.Image as Image
import json
import time
start = time.time()
def bakers(a,b,c):
 x=a
 y=b
 z=c
 if a>=0.0 and a<0.5 and b>=0 and b<0.5:
  x=2*a
  y=2*b
  z=c/2
 elif a>=0 and a<0.5 and b>=0.5 and b<=1:
  x=a*2
#***************************************************
  y=(b*2)-1
  z=(c/4)+0.5
 elif a>=0.5 and a<=1 and b>=0 and b<0.5:
  x=(2*a)-1
  y=b*2
  z=(c/4)+0.25
 elif a>=0.5 and a<=1 and b>=0.5 and b<=1:
  x=(2*a)-1
  y=(b*2)-1
  z=(c/4)+0.75
 l=int(x*255)
 m=int(y*255)
 n=int(z*255)
 return l, m, n
myImage = Image.open("false9.jpg")
width, height = myImage.size
pixels = myImage.load()
has_alpha = len(pixels[0,0]) == 4
arr=[]
for y1 in range(height):
 for x1 in range(width):
  if has_alpha:
   r, g, b, a = pixels[x1,y1]
  else:
   r, g, b = pixels[x1,y1]
   arr.append(r)
for y2 in range(height):
 for x2 in range(width):
  if has_alpha:
   r, g, b, a = pixels[x2,y2]
   k=(255-r)/255
   l=(255-g)/255
   m=(255-b)/255
#***************************************************
   r,g,b=bakers(k,l,m)
   value=(r,g,b,a)
   myImage.putpixel((int(x2), int(y2)), value)
  else:
   r, g, b = pixels[x2,y2]
   k=(255-r)/255
   l=(255-g)/255
   m=(255-b)/255
   r,g,b= bakers(k,l,m)
   value=(r,g,b)
   myImage.putpixel((int(x2), int(y2)), value)
myImage=myImage.convert('RGB')
myImage.save("chao.jpg")



high = (2**8) - 1
low = 0
myImage = Image.open("chao.jpg");
width, height = myImage.size
pixels = myImage.load()
print(pixels[0,0])
has_alpha = len(pixels[0,0]) == 4
fill = 1
#***************************************************************
array = [[fill for x in range(width)] for y in range(height)]
for y in range(height):
 for x in range(width):
  if has_alpha:
   r, g, b, a = pixels[x,y]
  else:
   r, g, b = pixels[x,y]
  array[y][x] = r 
KR = [40, 6, 227, 45, 19, 236, 8, 163, 50, 252, 21, 216, 143, 170, 114, 134, 46, 4, 185, 3, 34, 247, 175, 253, 
137, 111, 177, 254, 166, 186, 77, 183, 11, 31, 244, 169, 162, 137, 248, 252, 63, 221, 100, 7, 28, 152, 228, 5, 
82, 212, 164, 133, 124, 252, 55, 187, 64, 85, 1, 44, 156, 86, 252, 91, 224, 34, 70, 73, 231, 119, 216, 211, 147, 
5, 221, 96, 73, 63, 147, 126, 117, 80, 134, 130, 29, 56, 180, 201, 157, 28, 207, 233, 10, 147, 239, 73, 57, 0, 
214, 33, 32, 150, 72, 127, 119, 230, 102, 169, 232, 10, 111, 217, 235, 132, 78, 197, 53, 142, 94, 79, 16, 240, 
217, 149, 117, 188, 106, 120, 175, 98, 170, 181, 93, 45, 101, 4, 47, 236, 43, 41, 251, 52, 124, 202, 24, 76, 
144, 54, 58, 221, 184, 35, 177, 146, 42, 139, 232, 13, 51, 233, 43, 83, 241, 236, 48, 215, 26, 86, 20, 70, 34, 
217, 212, 4, 181, 45, 17, 121, 91, 202, 155, 240, 141, 86, 141, 192, 178, 175, 149, 173, 223, 116, 226, 87, 76, 
133, 185, 219, 64, 105, 245, 238, 251, 46, 100, 160, 134, 126, 229, 29, 199, 92, 21, 145, 61, 67, 89, 21, 127, 
104, 243, 183, 215, 220, 148, 6, 245, 230, 178, 195, 19, 192, 136, 99, 27, 157, 189, 108, 54, 107,41]
KC = [197, 98, 234, 162, 220, 198, 187, 211, 1, 224, 140, 104, 191, 7, 157, 210, 191, 134, 10, 210, 218, 22, 
56, 61, 196, 242, 21, 89, 226, 254, 3, 229, 213, 83, 242, 92, 122, 242, 227, 115, 92, 27, 131, 50, 178, 158, 29, 
127, 19, 12, 189, 16, 35, 220, 97, 249, 191, 190, 220, 126, 32, 215, 231, 224, 94, 7, 120, 215, 63, 220, 243, 
111, 110, 147, 230, 43, 240, 54, 97, 17, 254, 98, 105, 110, 132, 130, 58, 118, 217, 73, 175, 164, 18, 140, 23, 
187, 32, 189, 169, 23, 156, 246, 234, 236, 204, 5, 222, 92, 248, 172, 44, 246, 208, 68, 159, 15, 211, 182, 44, 
215, 237, 27, 23, 221, 85, 253, 103, 24, 31, 8, 46, 217, 56, 163, 28, 137, 131, 75, 203, 202, 12, 117, 150, 87, 
121, 168, 129, 164, 70, 222, 30, 157, 215, 13, 108, 77, 108, 242, 228, 167, 192, 17, 213, 34, 75, 56, 25, 89, 
230, 125, 169, 159, 216, 139, 158, 46, 33, 254, 67, 239, 54, 159, 175, 101, 41, 221, 61, 164, 66, 41, 113, 12,
7, 114, 254, 52, 40, 0, 180, 25, 184, 43, 84, 73, 65, 195, 182, 61, 35, 250, 81, 67, 52, 215, 255, 176, 112, 22, 
208, 108, 172, 98, 30, 238, 245, 233, 57, 83, 121, 48, 109, 150, 130, 170, 88, 121, 198, 234, 95, 59,81]
for i in range(height):
 alpha = 0
 for j in range(width):
  alpha = ((alpha%2) + (array[i][j] % 2)) % 2
#****************************************************************
 if(alpha == 0):
  for k in range(KR[i]):
   temp2 = array[i][width-1]
   for l in range(width-1, -1, -1):
    array[i][l] = array[i][l-1];
  array[i][0] = temp2;
 else:
  for k in range(KR[i]):
   temp2 = array[i][0]
   for l in range(width-1):
    array[i][l] = array[i][l+1];
   array[i][width-1] = temp2;
for j in range(width):
 beta = 0
 for i in range(height):
  beta = ((beta%2) + (array[i][j] % 2)) % 2
 if(beta == 0):
  for k in range(KC[j]):
   temp2 = array[height - 1][j]
   for l in range(height-1, -1, -1):
    array[l][j] = array[l-1][j];
   array[0][j] = temp2;
 else:
  for k in range(KC[j]):
   temp2 = array[0][j]
   for l in range(height-1):
    array[l][j] = array[l+1][j];
   array[height-1][j] = temp2; 
for j in range(width):
 for i in range(height):
#************************************************************
  if((i%2) !=0 ):
   array[i][j] = array[i][j]^KC[j]
  else:
   array[i][j] = array[i][j]^KC[width-1-j]
for i3 in range(height):
 for j3 in range(width):
  if((j3%2) !=0 ):
   array[i3][j3] = array[i3][j3]^KR[i3]
  else:
   array[i3][j3] = array[i3][j3]^KR[height-1-i3]
array1 = np.array(array, dtype=np.uint8)
new_image = Image.fromarray(array1)
new_image.save('C:\\Users\\hp\\OneDrive\\Desktop\\mini project\\demo\\beakers_encrypted.jpg')
with open("KR.txt", "w") as outfile:
 json.dump(KR, outfile)
with open("KC.txt", "w") as outfile:
 json.dump(KC, outfile)
 
# Close all windows
c.destroyAllWindows()
end=time.time()
print("Time of Execution -> ", end-start)
