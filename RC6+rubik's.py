import base64 as b6
import math 
import cv2 as c
from Crypto.Util.Padding import *
from PIL import BmpImagePlugin
import time
from PIL import Image
import numpy as np
import json
start = time.time()
class RC6:
 def ToXor(self, *Args):
  lgt = len(bin(max(Args))[2:])
  Args = [self.binExp(bin(arg), lgt)[2:] for arg in Args]

  op = '0b'
  for x in range(lgt):
    counter = 0
    for arg in Args:
     counter += int(arg[x])
    op += str(counter % 2)
  return int(op, 2)
 def binExp(self, bit_string, length):
  output = bit_string
  while len(output) != length + 2:
   output = output[:2] + '0' + output[2:]
  return output
 def SCircular(self, number, w, bits, side):
  binString = self.binExp(bin(number), w)
  bits %= w 
  binString = binString[2:]
  if side == 'left':
   return int('0b' + binString[bits:] + binString[:bits], 2)
  if side == 'right':
   return int('0b' + binString[-bits:] + binString[:-bits], 2)
 def keysTableGen(self, key, w = 32, r = 20):
  mod = 2 ** w
  while len(key) % w != 0:
   key = key + '0'
  c = int(len(key) / w) # no. of words in a key
  L = [key[i * w : (i + 1) * w] for i in range(c)]
  L = [int('0b' + k, 2) for k in L]
  def odd(number):
   """Rounding to the nearest odd integer"""

   if int(number) % 2 != 0: return int(number) 
   else: return int(number) + 1
  f = (math.sqrt(5) + 1) / 2 # golden ratio 
  Qw = odd((f - 1) * 2 ** w)
  Pw = odd((math.e - 2) * 2 ** w)
  S = []
  S.append(Pw)
  for p in range(1, 2 * r + 4):
    S.append((S[p - 1] + Qw) % mod)
  A = B = i = j = 0
  V1 = 3 * max(c , 2 * r + 4)
  for q in range(1, V1):
    A = S[i] = self.SCircular((S[i] + A + B) % mod, w, 3, 'left')
    B = L[j] = self.SCircular((L[j] + A + B) % mod, w, (A + B) % mod, 'left')
    i = (i + 1) % (2 * r + 4)
    j = (j + 1) % c
  self.keysTable = S
  return S
 def binEncryption(self, msg, w = 32, r = 20):
  mod = 2 ** w
  S = self.keysTable
  A = int('0b' + msg[0:w], 2)
  B = int('0b' + msg[(w):(2 * w)], 2)
  C = int('0b' + msg[(2 * w):(3 * w)], 2)
  D = int('0b' + msg[(3 * w):(4 * w)], 2)

  B = (B + S[0]) % mod
  D = (D + S[1]) % mod
  for i in range(1, r):
   t = self.SCircular((B * ((2 * B) % mod + 1) % mod) % mod, w, int(math.log(w)), 'left')
   u = self.SCircular((D * ((2 * D) % mod + 1) % mod) % mod, w, int(math.log(w)), 'left')
   A = (self.SCircular(self.ToXor(A, t), w, u, 'left') + S[2 * i]) % mod
   C = (self.SCircular(self.ToXor(C, u), w, t, 'left') + S[2 * i + 1]) % mod
   aa, bb, cc, dd = B, C, D, A
   A, B, C, D = aa, bb, cc, dd 
  A = (A + S[2 * r + 2]) % mod
  C = (C + S[2 * r + 3]) % mod
  op = ''
  op += self.binExp(bin(A), w)[2:]
  op += self.binExp(bin(B), w)[2:]
  op += self.binExp(bin(C), w)[2:]
  op += self.binExp(bin(D), w)[2:]
  return (op)
 def ConvBytesBin(self, bytes):
  op = bytearray(bytes)
  op = [self.binExp(bin(char), 8)[2:] for char in op]
  op = ''.join(op)
  return op
 def ConvBinBytes(self, bin):
  output = [int('0b' + bin[block * 8 : (block + 1) * 8], 2) for block in range(int(len(bin) / 8))]
  output = bytes(output)
  return output
 def encryption(self, msg, key, w = 32, r = 20):
  self.keysTableGen(key, w = 32, r = 20)
  size = len(msg)
  size = self.binExp(bin(size), 64)
  msg = size[2:] + msg
  while len(msg) % (4 * w) != 0:
   msg += '0'
  msg = [msg[(block * 4 * w): ((block + 1) * 4 * w)] for block in range(int(len(msg) / (4 * w)))]
  output = ''
  for block in msg :
   output += self.binEncryption(block, w, r)
  return output
Original = c.imread("true1.jpg") 
Original_row, Original_col, Original_dep = Original.shape
# Display original image
c.imshow("Original_image", Original)
c.waitKey()
c.imwrite("tooriginalimg.bmp", Original)
Original = c.imread("tooriginalimg.bmp")
Original = BmpImagePlugin.BmpImageFile("tooriginalimg.bmp")
# Convert original image data to bytes
Original_bytes = Original.tobytes()
k = b6.b64encode(bytes("""Rc6encrypt""", 'utf-8'))
rc = RC6()
msgBin = rc.ConvBytesBin(Original_bytes)
keyBin = rc.ConvBytesBin(k)
encrpytedBin = rc.encryption(msgBin, keyBin)
encryptedBytes = rc.ConvBinBytes(encrpytedBin)
# Convert bytes to encrypted image data
opimage = Original.copy()
opimage.frombytes(encryptedBytes)
opimage.save("rc6encrypted.bmp")

#Rubik's Cube :
myImage = Image.open("rc6encrypted.bmp");
width, height = myImage.size
pixels = myImage.load()
has_alpha = len(pixels[0,0]) == 4 
fill = 1
array = [[fill for x1 in range(width)] for y1 in range(height)]
for y2 in range(height):
 for x2 in range(width):
  if has_alpha:
   r, g, b, a = pixels[x2,y2]
  else:
   r, g, b = pixels[x2,y2]
  array[y2][x2] = r 
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
 alpha1 = 0
 for j in range(width):
  alpha1 = ((alpha1%2) + (array[i][j] % 2)) % 2
 if(alpha1 == 0):
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
for j2 in range(width):
 for i2 in range(height):
  if((i2%2) !=0 ):
   array[i2][j2] = array[i2][j2]^KC[j2]
  else:
   array[i2][j2] = array[i2][j2]^KC[width-1-j2]
for i in range(height):
 for j in range(width):
  if((j%2) !=0 ):
   array[i][j] = array[i][j]^KR[i]
  else:
   array[i][j] = array[i][j]^KR[height-1-i]
array1 = np.array(array, dtype=np.uint8)
new_image = Image.fromarray(array1)
new_image.save("C:\\Users\\hp\\OneDrive\\Desktop\\mini project\\demo\\rc6_encrypted.jpg")
with open("D:\\Pictures\\TRIP\\THE BOYS+GRP\\mm\\KR.txt", "w") as outfile:
 json.dump(KR, outfile)
with open("D:\\Pictures\\TRIP\\THE BOYS+GRP\\mm\\KC.txt", "w") as outfile:
 json.dump(KC, outfile)
# Close all windows
c.destroyAllWindows()
end=time.time()
print("Time of Execution -> ", end-start)





