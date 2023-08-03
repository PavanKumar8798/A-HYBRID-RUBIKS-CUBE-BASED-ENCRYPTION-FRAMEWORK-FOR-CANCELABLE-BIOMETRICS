import cv2
import numpy as np
from scipy.stats import pearsonr
original_image = cv2.imread('rc6_2.jpg')
encrypted_image = cv2.imread('false_rc6_7.jpg')
original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
encrypted_gray = cv2.cvtColor(encrypted_image, cv2.COLOR_BGR2GRAY)
corr_coef, _ = pearsonr(original_gray.flatten(), encrypted_gray.flatten())
print("Correlation coefficient between original and encrypted image:", corr_coef)
